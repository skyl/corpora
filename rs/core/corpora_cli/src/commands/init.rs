use crate::context::Context;
use std::io::Write;
use std::{fs, io, path::Path};

pub fn run(ctx: &Context) {
    ctx.success("Starting corpus initialization...");

    let corpus_name = ctx.corpora_config.name.clone();
    ctx.print(
        &format!("Using corpus name: {}", corpus_name),
        console::Style::new().blue(),
    );

    let url = Some(ctx.corpora_config.url.clone());
    ctx.print(
        &format!(
            "Using repository URL: {}",
            url.clone().unwrap_or_else(|| "None".to_string())
        ),
        console::Style::new().blue(),
    );

    // Start progress bar for tarball collection
    ctx.print(
        "Collecting files for tarball...",
        console::Style::new().cyan(),
    );
    let tarball_progress = ctx.progress_bar(100, "Creating tarball...");

    let tarball_path = match ctx.collector.collect_tarball() {
        Ok(path) => {
            tarball_progress.finish_with_message("Tarball created successfully!");
            ctx.success(&format!("Tarball generated at: {}", path.display()));
            path
        }
        Err(err) => {
            tarball_progress.abandon_with_message("Failed to create tarball.");
            ctx.error(&format!("Failed to create tarball: {:?}", err));
            return;
        }
    };
    let tarball_size = fs::metadata(&tarball_path).unwrap().len();
    let tarball_size_mb = (tarball_size as f64) / (1024.0 * 1024.0);
    ctx.print(
        &format!("Tarball size: {:.8} MB", tarball_size_mb),
        console::Style::new().blue(),
    );

    // Confirm with the user
    if !ctx.prompt_confirm("Do you want to proceed with creating a new corpus?") {
        ctx.warn("Initialization aborted by the user.");
        // Clean up the temporary tarball file
        ctx.print(
            "Cleaning up temporary files...",
            console::Style::new().cyan(),
        );
        if let Err(err) = fs::remove_file(&tarball_path) {
            ctx.warn(&format!("Failed to remove temporary tarball: {:?}", err));
        } else {
            ctx.success("Temporary tarball file removed successfully.");
        }
        return;
    }

    // Start progress bar for API call
    ctx.print("Sending tarball to server...", console::Style::new().cyan());
    let api_progress = ctx.progress_bar(1, "Creating corpus...");

    match corpora_client::apis::corpus_api::create_corpus(
        &ctx.api_config,
        &corpus_name,
        tarball_path.clone(),
        url.as_deref(),
    ) {
        Ok(response) => {
            api_progress.finish_with_message("Corpus created successfully!");
            ctx.success(&format!(
                "Corpus created successfully with ID: {}",
                response.id
            ));

            // Write the response ID to `.corpora/.id`
            if let Err(err) = write_corpus_id(&ctx.corpora_config.root_path, &response.id) {
                ctx.error(&format!("Failed to write corpus ID: {:?}", err));
            } else {
                ctx.success("Corpus ID saved to `.corpora/.id`.");
            }
        }
        Err(err) => {
            // TODO: probably can do a lot better here with CreateCorpusError
            api_progress.abandon_with_message("Failed to create corpus.");
            ctx.error(&format!("Failed to create corpus: {:?}", err));
        }
    }

    // Clean up the temporary tarball file
    ctx.print(
        "Cleaning up temporary files...",
        console::Style::new().cyan(),
    );
    if let Err(err) = fs::remove_file(&tarball_path) {
        ctx.warn(&format!("Failed to remove temporary tarball: {:?}", err));
    } else {
        ctx.success("Temporary tarball file removed successfully.");
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
