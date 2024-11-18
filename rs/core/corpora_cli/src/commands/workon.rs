use crate::context::Context;
use clap::Args;
use corpora_client::models::{CorpusFileChatSchema, MessageSchema};
use dialoguer::{theme::ColorfulTheme, Confirm, Input};
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;

#[derive(Args)]
pub struct WorkonArgs {
    #[arg(help = "Path to the file or directory")]
    pub path: String,
}

/// The `workon` command operation
pub fn run(ctx: &Context, args: WorkonArgs) {
    // get path as a path from the string
    let path = Path::new(&args.path);
    // get cwd
    let cwd = std::env::current_dir().unwrap();
    ctx.print(
        &format!("Current working directory: {}", cwd.display()),
        dialoguer::console::Style::new().dim(),
    );
    // add cwd and args.path
    let absolute_path = Path::join(&cwd, path);
    // rm the config.root_path to get the relative path
    let relative_path = absolute_path
        .strip_prefix(&ctx.corpora_config.root_path)
        .unwrap();
    // ctx.success(&format!("Working on file: {}", relative_path.display()));
    ctx.print(
        &format!("Working on file: {}", relative_path.display()),
        dialoguer::console::Style::new().dim().green(),
    );
    let ext = relative_path
        .extension()
        .unwrap_or_default()
        .to_str()
        .unwrap_or("");

    // Show current file content, load the content from the
    let current_file_content = match fs::read_to_string(path) {
        Ok(content) => content,
        Err(_) => {
            File::create(&path).expect("Failed to create file");
            String::new()
        }
    };

    ctx.success("Current file content:");
    ctx.print(
        &current_file_content,
        dialoguer::console::Style::new().dim(),
    );

    let mut messages: Vec<MessageSchema> = Vec::new();

    if !current_file_content.is_empty() {
        messages.push(MessageSchema {
            role: "user".to_string(),
            text: format!(
                "The original content of `{}` was:\n```{}\n```",
                relative_path.display(),
                current_file_content
            ),
        });
    }

    // REPL loop
    loop {
        let user_input: String = Input::with_theme(&ColorfulTheme::default())
            .with_prompt(if messages.is_empty() {
                "What to do?"
            } else {
                "How to revise?"
            })
            .allow_empty(false)
            .interact_text()
            .unwrap();

        // Add the user's input as a new message
        messages.push(MessageSchema {
            role: "user".to_string(),
            text: user_input.trim().to_string(),
        });

        // Generate revision
        ctx.success("Generating revision...");

        let root_path = &ctx.corpora_config.root_path;
        let voice = fs::read_to_string(root_path.join(".corpora/VOICE.md")).unwrap_or_default();
        let purpose = fs::read_to_string(root_path.join(".corpora/PURPOSE.md")).unwrap_or_default();
        let structure =
            fs::read_to_string(root_path.join(".corpora/STRUCTURE.md")).unwrap_or_default();
        let directions =
            fs::read_to_string(root_path.join(format!(".corpora/{}/DIRECTIONS.md", ext)))
                .unwrap_or_default();

        let revision = match corpora_client::apis::workon_api::file(
            &ctx.api_config,
            CorpusFileChatSchema {
                messages: messages.clone(),
                corpus_id: ctx
                    .corpora_config
                    .id
                    .clone()
                    .expect("Failed to get corpus ID"),
                path: relative_path.to_string_lossy().to_string(),
                voice: Some(voice),
                purpose: Some(purpose),
                structure: Some(structure),
                directions: Some(directions),
            },
        ) {
            Ok(response) => response,
            Err(err) => {
                ctx.error(&format!("Failed to generate revision: {:?}", err));
                continue;
            }
        };

        ctx.print(&revision, dialoguer::console::Style::new().dim());
        // println!("{}", relative_path.display());
        ctx.print(
            &format!("Revision for `{}`:", relative_path.display()),
            dialoguer::console::Style::new().dim().magenta().on_green(),
        );
        messages.push(MessageSchema {
            role: "assistant".to_string(),
            text: revision.clone(),
        });

        if Confirm::with_theme(&ColorfulTheme::default())
            .with_prompt("Write file?")
            .interact()
            .unwrap()
        {
            let mut file = File::create(&path).expect("Failed to open file");
            file.write_all(revision.as_bytes())
                .expect("Failed to write file");
            ctx.success("File written!");
        } else {
            ctx.warn("You chose not to write the file. Give more input to revise.");
        }
    }
}
