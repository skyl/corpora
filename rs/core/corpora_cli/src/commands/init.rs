use crate::context::Context;
use flate2::write::GzEncoder;
use flate2::Compression;
use std::{fs, io, path::Path, process::Command};

pub fn run(ctx: &Context) {
    println!("Initializing a new corpus...");

    let corpus_name = ctx.corpora_config.name.clone();
    let url = Some(ctx.corpora_config.url.clone());

    // Determine the root path of the repository (where .corpora.yaml is located)
    let root_path = match find_repo_root() {
        Some(path) => path,
        None => {
            eprintln!("Failed to determine the root of the repository.");
            return;
        }
    };

    // Generate a tarball of all tracked files and save to a temporary file
    let tarball_path = match create_tarball_from_git(&root_path) {
        Ok(path) => path,
        Err(err) => {
            eprintln!("Failed to create tarball: {:?}", err);
            return;
        }
    };

    // Call the API to create a new corpus
    match corpora_client::apis::corpus_api::create_corpus(
        &ctx.api_config,
        &corpus_name,
        tarball_path.clone(),
        url.as_deref(),
    ) {
        Ok(response) => {
            println!("Corpus created successfully: {:?}", response);
        }
        Err(err) => {
            eprintln!("Failed to create corpus: {:?}", err);
        }
    }

    // Clean up the temporary tarball file
    if let Err(err) = fs::remove_file(tarball_path) {
        eprintln!("Failed to remove temporary tarball: {:?}", err);
    }
}

/// Find the root directory of the Git repository
fn find_repo_root() -> Option<std::path::PathBuf> {
    let repo = git2::Repository::discover(".").ok()?;
    repo.workdir().map(|path| path.to_path_buf())
}

/// Create a tarball of all tracked files in the Git repository and save to a temporary file
fn create_tarball_from_git(root_path: &Path) -> io::Result<std::path::PathBuf> {
    // Get the list of tracked files using `git ls-files`
    let output = Command::new("git")
        .arg("ls-files")
        .current_dir(root_path)
        .output()?;

    if !output.status.success() {
        return Err(io::Error::new(
            io::ErrorKind::Other,
            "Failed to list tracked files with git.",
        ));
    }

    // Parse the output into a list of file paths
    let files = String::from_utf8_lossy(&output.stdout)
        .lines()
        .map(|line| root_path.join(line))
        .collect::<Vec<_>>();

    // Create a temporary file for the tarball
    let tarball_path = root_path.join("temp_tarball.tar.gz");

    let tar_gz_file = fs::File::create(&tarball_path)?;
    let mut encoder = GzEncoder::new(tar_gz_file, Compression::default());

    {
        // Create a tar archive in the gzip encoder
        let mut tar = tar::Builder::new(&mut encoder);

        for file_path in files {
            if file_path.is_file() {
                let file_name = file_path.strip_prefix(root_path).unwrap();
                let mut file = fs::File::open(&file_path)?;
                tar.append_file(file_name, &mut file)?;
            }
        }

        tar.finish()?;
    }

    encoder.finish()?;
    Ok(tarball_path)
}
