use crate::context::config::CorporaConfig;
use std::error::Error;

/// Trait defining the behavior of a file collector
pub trait Collector {
    /// Collects a list of `PathBuf` objects representing all available paths
    ///
    /// # Errors
    /// Returns an error if the collector fails to gather paths.
    fn collect_paths(&self) -> Result<Vec<std::path::PathBuf>, Box<dyn Error>>;

    /// Creates a tarball containing all files tracked by the collector
    ///
    /// # Errors
    /// Returns an error if the tarball creation fails.
    fn collect_tarball(&self) -> Result<std::path::PathBuf, Box<dyn Error>>;

    /// Creates a tarball containing only the specified paths
    ///
    /// # Arguments
    /// * `paths` - A list of paths to include in the tarball.
    ///
    /// # Errors
    /// Returns an error if the tarball creation fails.
    fn collect_tarball_for_paths(
        &self,
        paths: Vec<&std::path::PathBuf>,
    ) -> Result<std::path::PathBuf, Box<dyn Error>>;
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
    // println!("Root path: {:?}", config.root_path);
    git2::Repository::discover(&config.root_path).is_ok()
}

pub mod git;
