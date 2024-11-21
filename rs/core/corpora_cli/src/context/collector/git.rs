use super::Collector;
use crate::context::config::CorporaConfig;
use flate2::write::GzEncoder;
use flate2::Compression;
use globset::{Glob, GlobSet, GlobSetBuilder};
use std::error::Error;
use std::fs::{self, File};
use std::path::{Path, PathBuf};
use std::process::Command;

/// A collector implementation for Git repositories
pub struct GitCollector {
    root_path: PathBuf,
    exclude_globs: GlobSet,
}

impl GitCollector {
    /// Creates a new instance of `GitCollector`
    ///
    /// # Arguments
    /// * `config` - The `CorporaConfig` containing the root path and exclude_globs information.
    pub fn new(config: &CorporaConfig) -> Self {
        // Build a GlobSet from the exclude globs in the configuration
        let mut glob_builder = GlobSetBuilder::new();
        if let Some(exclude_patterns) = &config.exclude_globs {
            for pattern in exclude_patterns {
                glob_builder.add(Glob::new(pattern).expect("Invalid glob pattern in config"));
            }
        }
        let exclude_globs = glob_builder
            .build()
            .expect("Failed to build globset from exclude patterns");

        Self {
            root_path: PathBuf::from(&config.root_path),
            exclude_globs,
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
    /// Collects a list of `PathBuf` objects representing tracked text files
    fn collect_paths(&self) -> Result<Vec<PathBuf>, Box<dyn Error>> {
        println!("Starting to collect paths");

        // Get a list of tracked files using `git ls-files`
        let output = Command::new("git")
            .arg("ls-files")
            .current_dir(&self.root_path)
            .output()
            .map_err(|e| format!("Failed to execute git command: {}", e))?;

        if !output.status.success() {
            return Err(format!("Git command failed with status {}", output.status).into());
        }

        let tracked_files: Vec<PathBuf> = String::from_utf8_lossy(&output.stdout)
            .lines()
            .map(|line| self.root_path.join(line)) // Join the root path for full paths
            .filter(|path| {
                Self::is_text_file(path) // Check if it's a text file
                    && !self
                        .exclude_globs
                        .is_match(path.strip_prefix(&self.root_path).unwrap_or(path))
                // Match relative paths to globs
            })
            .collect();

        println!("Filtered paths: {:?}", tracked_files.len());
        Ok(tracked_files)
    }
    /// Creates a tarball containing all tracked text files and returns the `PathBuf` to the tarball
    fn collect_tarball(&self) -> Result<PathBuf, Box<dyn Error>> {
        println!("Starting to collect tarball");
        let files = self.collect_paths()?;
        println!("Files to include in tarball: {:?}", files.len());
        self.collect_tarball_for_paths(files.iter().collect())
    }

    /// Creates a tarball containing only the specified paths
    ///
    /// # Arguments
    /// * `paths` - A vector of references to `PathBuf` to include in the tarball.
    ///
    /// # Errors
    /// Returns an error if the tarball creation fails.
    fn collect_tarball_for_paths(&self, paths: Vec<&PathBuf>) -> Result<PathBuf, Box<dyn Error>> {
        let tarball_path = self.root_path.join("temp_tarball_selected.tar.gz");
        let tar_gz_file = File::create(&tarball_path)?;
        let mut encoder = GzEncoder::new(tar_gz_file, Compression::default());

        {
            let mut tar = tar::Builder::new(&mut encoder);
            for file_path in paths {
                if file_path.is_file() {
                    let file_name = file_path.strip_prefix(&self.root_path)?;
                    let mut file = File::open(file_path)?;
                    tar.append_file(file_name, &mut file)?;
                }
            }
            tar.finish()?;
        }

        encoder.finish()?;
        Ok(tarball_path)
    }
}
