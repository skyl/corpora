use super::Collector;
use crate::context::config::CorporaConfig;
use flate2::write::GzEncoder;
use flate2::Compression;
use std::error::Error;
use std::fs::{self, File};
use std::path::{Path, PathBuf};
use std::process::Command;

/// A collector implementation for Git repositories
pub struct GitCollector {
    root_path: PathBuf,
    // config: CorporaConfig,
}

impl GitCollector {
    /// Creates a new instance of `GitCollector`
    ///
    /// # Arguments
    /// * `config` - The `CorporaConfig` containing the root path information.
    pub fn new(config: &CorporaConfig) -> Self {
        Self {
            // config: config.clone(),
            root_path: PathBuf::from(&config.root_path),
        }
    }

    /// Filters files to include only text files
    fn is_text_file(path: &Path) -> bool {
        if let Ok(contents) = fs::read(path) {
            return contents.is_empty() || std::str::from_utf8(&contents).is_ok();
        }
        false
    }
}

impl Collector for GitCollector {
    // /// Collects a list of tracked files in the Git repository
    // fn collect_files(&self) -> Result<Vec<String>, Box<dyn Error>> {
    //     let output = Command::new("git")
    //         .arg("ls-files")
    //         .current_dir(&self.root_path)
    //         .output()
    //         .map_err(|e| format!("Failed to execute git command: {}", e))?;

    //     if !output.status.success() {
    //         return Err(format!("Git command failed with status {}", output.status).into());
    //     }

    //     let files = String::from_utf8_lossy(&output.stdout)
    //         .lines()
    //         .filter(|line| Self::is_text_file(&self.root_path.join(line)))
    //         .map(|line| line.to_string())
    //         .collect();

    //     Ok(files)
    // }

    /// Collects a list of `PathBuf` objects representing tracked text files
    fn collect_paths(&self) -> Result<Vec<PathBuf>, Box<dyn Error>> {
        let output = Command::new("git")
            .arg("ls-files")
            .current_dir(&self.root_path)
            .output()
            .map_err(|e| format!("Failed to execute git command: {}", e))?;

        if !output.status.success() {
            return Err(format!("Git command failed with status {}", output.status).into());
        }

        let paths = String::from_utf8_lossy(&output.stdout)
            .lines()
            .map(|line| self.root_path.join(line))
            .filter(|path| Self::is_text_file(path))
            .collect();

        Ok(paths)
    }

    /// Creates a tarball containing all tracked text files and returns the `PathBuf` to the tarball
    fn collect_tarball(&self) -> Result<PathBuf, Box<dyn Error>> {
        let files = self.collect_paths()?;
        let tarball_path = self.root_path.join("temp_tarball.tar.gz");
        let tar_gz_file = File::create(&tarball_path)?;
        let mut encoder = GzEncoder::new(tar_gz_file, Compression::default());

        {
            let mut tar = tar::Builder::new(&mut encoder);
            for file_path in files {
                if file_path.is_file() {
                    let file_name = file_path.strip_prefix(&self.root_path)?;
                    let mut file = File::open(&file_path)?;
                    tar.append_file(file_name, &mut file)?;
                }
            }
            tar.finish()?;
        }

        encoder.finish()?;
        Ok(tarball_path)
    }
}
