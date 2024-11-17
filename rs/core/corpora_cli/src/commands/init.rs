use crate::context::Context;
use std::io::Write;
use std::{fs, io, path::Path};

pub fn run(ctx: &Context) {
    println!("Initializing a new corpus...");

    let corpus_name = ctx.corpora_config.name.clone();
    let url = Some(ctx.corpora_config.url.clone());

    // Use the collector to generate a tarball of all tracked files
    let tarball_path = match ctx.collector.collect_tarball() {
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

            // Write the response ID to `.corpora/.id`
            if let Err(err) = write_corpus_id(&ctx.corpora_config.root_path, &response.id) {
                eprintln!("Failed to write corpus ID: {:?}", err);
            }
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

/// Write the corpus ID to `.corpora/.id` in the root path
fn write_corpus_id(root_path: &Path, id: &uuid::Uuid) -> io::Result<()> {
    let corpora_dir = root_path.join(".corpora");
    let id_file_path = corpora_dir.join(".id");

    // Ensure `.corpora` directory exists
    if !corpora_dir.exists() {
        fs::create_dir_all(&corpora_dir)?;
    }

    // Write the ID to `.corpora/.id`
    let mut id_file = fs::File::create(id_file_path)?;
    writeln!(id_file, "{}", id)?;

    Ok(())
}
