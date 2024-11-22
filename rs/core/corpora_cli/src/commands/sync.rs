use crate::context::Context;
use std::{collections::HashMap, fs, path::PathBuf};

// Implement the `cleanup_temp_files` function
// // Clean up the tarball
// ctx.success("Cleaning up temporary tarball file...");
// if let Err(err) = fs::remove_file(&tarball_path) {
//     ctx.warn(&format!("Failed to remove temporary tarball: {:?}", err));
// } else {
//     ctx.success("Temporary tarball file removed successfully.");
// }

/// Clean up a list of temporary files
pub fn cleanup_temp_files(files: &[PathBuf], ctx: &Context) {
    for file in files {
        ctx.success(&format!("Cleaning up temporary file: {}", file.display()));
        if let Err(err) = fs::remove_file(file) {
            ctx.warn(&format!("Failed to remove temporary file: {:?}", err));
        } else {
            ctx.success("Temporary file removed successfully.");
        }
    }
}

/// Run the `sync` command
pub fn run(ctx: &Context) {
    ctx.success("Starting corpus sync...");

    // Ensure corpus ID exists in the configuration
    let corpus_id = match &ctx.corpora_config.id {
        Some(id) => id.clone(),
        None => {
            ctx.error("Corpus ID not found in the configuration. Please run 'init' first.");
            return;
        }
    };
    ctx.success(&format!("Corpus ID: {}", corpus_id));

    // Collect local files and their hashes
    ctx.success("Collecting local files...");
    let local_files = match ctx.collector.collect_paths() {
        Ok(paths) => paths,
        Err(err) => {
            ctx.error(&format!("Failed to collect local files: {:?}", err));
            return;
        }
    };

    // Compute local file hashes
    let local_files_hash_map: HashMap<String, String> = local_files
        .iter()
        .filter_map(|file| {
            let hash = get_file_hash(file);
            hash.map(|h| {
                (
                    file.strip_prefix(&ctx.corpora_config.root_path)
                        .unwrap()
                        .to_string_lossy()
                        .to_string(),
                    h,
                )
            })
        })
        .collect();

    // Fetch remote file hashes
    ctx.success("Fetching remote file hashes...");
    let remote_files_map: HashMap<String, String> =
        match corpora_client::apis::corpus_api::get_file_hashes(&ctx.api_config, &corpus_id) {
            Ok(remote_files) => remote_files,
            Err(err) => {
                ctx.error(&format!("Failed to fetch remote file hashes: {:?}", err));
                return;
            }
        };

    // Determine files to update/add and delete
    let files_to_update: HashMap<String, String> = local_files_hash_map
        .iter()
        .filter(|(path, hash)| {
            remote_files_map
                .get(*path) // `*path` is a `String`, matching the remote map keys
                .map_or(true, |remote_hash| remote_hash != *hash)
        })
        .map(|(path, hash)| (path.clone(), hash.clone()))
        .collect();

    let files_to_delete: Vec<String> = remote_files_map
        .keys()
        .filter(|path| !local_files_hash_map.contains_key(*path))
        .cloned()
        .collect();

    ctx.warn(&format!("Files to update/add ({}):", files_to_update.len()));
    for file in files_to_update.keys() {
        ctx.dim(&format!(" - {}", file));
    }
    ctx.warn(&format!("Files to delete ({}):", files_to_delete.len()));
    for file in &files_to_delete {
        ctx.dim(&format!(" - {}", file));
    }
    if files_to_update.is_empty() && files_to_delete.is_empty() {
        ctx.success("No changes detected. Everything is up-to-date!");
        return;
    }

    // Create tarball for files to update/add
    ctx.success("Creating tarball for updated/added files...");
    let paths_to_update: Vec<PathBuf> = files_to_update
        .keys()
        .map(|path| ctx.corpora_config.root_path.join(path))
        .collect();

    let paths_to_update_refs: Vec<&PathBuf> = paths_to_update.iter().collect();

    let tarball_path = match ctx
        .collector
        .collect_tarball_for_paths(paths_to_update_refs)
    {
        Ok(tarball) => {
            ctx.success("Tarball created successfully!");
            tarball
        }
        Err(err) => {
            ctx.error(&format!("Failed to create tarball: {:?}", err));
            return;
        }
    };

    let upload = ctx.prompt_confirm("Do you want to upload?");
    if !upload {
        cleanup_temp_files(&[tarball_path], ctx);
        ctx.warn("Aborting sync. No changes have been made.");
        return;
    }

    match corpora_client::apis::corpus_api::update_files(
        &ctx.api_config,
        &corpus_id,
        tarball_path.clone(),
        Some(files_to_delete),
    ) {
        Ok(_) => {
            ctx.success("Corpus sync completed successfully!");
        }
        Err(err) => {
            ctx.error(&format!("Failed to sync corpus: {:?}", err));
        }
    }

    cleanup_temp_files(&[tarball_path], ctx);
}

/// Calculate a hash for the given file path
fn get_file_hash(path: &PathBuf) -> Option<String> {
    use sha1::{Digest, Sha1}; // Use `sha1` crate for Git-compatible hashing
    use std::fs;

    // Read the file content
    let content = match fs::read(path) {
        Ok(content) => content,
        Err(_) => return None,
    };

    // Compute the Git-compatible hash
    let size = content.len();
    let mut hasher = Sha1::new();

    // Add the Git "blob" header: "blob <size>\0"
    hasher.update(format!("blob {}\0", size).as_bytes());
    hasher.update(&content);

    // Return the hexadecimal representation of the hash
    Some(format!("{:x}", hasher.finalize()))
}
