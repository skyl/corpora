use crate::context::config::CorporaConfig;
use std::error::Error;

/// Trait defining the behavior of a file collector
pub trait Collector {
    /// Collects files and returns a list of file paths as strings
    ///
    /// # Errors
    /// Returns an error if the collector fails to gather files.
    // fn collect_files(&self) -> Result<Vec<String>, Box<dyn Error>>;
    fn collect_paths(&self) -> Result<Vec<std::path::PathBuf>, Box<dyn Error>>;
    fn collect_tarball(&self) -> Result<std::path::PathBuf, Box<dyn Error>>;
}

/// Gets the appropriate file collector based on the configuration
///
/// # Arguments
/// * `config` - The `CorporaConfig` containing the repository information.
///
/// # Returns
/// A boxed implementation of `Collector`.
///
/// # Errors
/// Returns an error if no suitable collector is available or initialization fails.
pub fn get_collector(config: &CorporaConfig) -> Result<Box<dyn Collector>, Box<dyn Error>> {
    if is_git_repo(config) {
        Ok(Box::new(crate::context::collector::git::GitCollector::new(
            config,
        )))
    } else {
        Err("No suitable file collector found for the given configuration.".into())
    }
}

/// Checks if the repository is a Git repository
///
/// # Arguments
/// * `config` - The `CorporaConfig` containing the repository information.
///
/// # Returns
/// A boolean indicating whether the repository is a Git repository.
fn is_git_repo(config: &CorporaConfig) -> bool {
    // print the root_path
    println!("Root path: {:?}", config.root_path);
    return git2::Repository::discover(&config.root_path).is_ok();
}

pub mod git;
