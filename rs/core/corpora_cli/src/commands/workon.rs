use crate::context::Context;
use clap::Args;
use corpora_client::models::{CorpusFileChatSchema, MessageSchema};
use dialoguer::{theme::ColorfulTheme, Confirm};
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;

#[derive(Args)]
pub struct WorkonArgs {
    #[arg(help = "Path to the file or directory")]
    pub path: String,

    #[arg(short, long, help = "name of persistent session")]
    pub persist: Option<String>,
}

/// The `workon` command operation
pub fn run(ctx: &Context, args: WorkonArgs) {
    let path = Path::new(&args.path);
    let cwd = std::env::current_dir().expect("Failed to get current directory");
    ctx.dim(&format!("Current working directory: {}", cwd.display()));
    let absolute_path = cwd.join(path);
    let relative_path = absolute_path
        .strip_prefix(&ctx.corpora_config.root_path)
        .expect("Failed to get relative path");

    ctx.magenta(&format!("Working on file: {}", relative_path.display()));
    let ext = relative_path
        .extension()
        .and_then(|s| s.to_str())
        .unwrap_or("");

    let current_file_content = match fs::read_to_string(path) {
        Ok(content) => content,
        Err(_) => {
            File::create(path).expect("Failed to create file");
            String::new()
        }
    };
    ctx.success("Current file content:");
    ctx.dim(&current_file_content);

    let mut messages: Vec<MessageSchema> = if let Some(session_name) = &args.persist {
        match ctx.history.load_session(session_name) {
            Ok(mut existing_messages) => {
                ctx.success(&format!("Loaded session: {}", session_name));
                for message in &existing_messages {
                    ctx.dim(&format!("{}: {}", message.role, message.text));
                }
                // add the original content of the file to the chat history
                if !current_file_content.is_empty() {
                    existing_messages.push(MessageSchema {
                        role: "user".to_string(),
                        text: format!(
                            "The current content of `{}` is:\n```\n{}\n```",
                            relative_path.display(),
                            current_file_content
                        ),
                    });
                }
                existing_messages
            }
            Err(_) => {
                ctx.warn(&format!("No existing session found for: {}", session_name));
                Vec::new()
            }
        }
    } else {
        if !current_file_content.is_empty() {
            vec![MessageSchema {
                role: "user".to_string(),
                text: format!(
                    "The original content of `{}` was:\n```\n{}\n```",
                    relative_path.display(),
                    current_file_content
                ),
            }]
        } else {
            Vec::new()
        }
    };

    loop {
        let user_input = ctx
            .get_user_input_via_editor(&format!(
                "Put your prompt here for {}, save and close",
                path.display()
            ))
            .expect("Failed to get user input");

        messages.push(MessageSchema {
            role: "user".to_string(),
            text: user_input.trim().to_string(),
        });

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

        ctx.dim(&revision);
        ctx.highlight(&format!("^^Revision for `{}`^^", relative_path.display()));
        messages.push(MessageSchema {
            role: "assistant".to_string(),
            text: revision.clone(),
        });

        if let Some(session_name) = &args.persist {
            if let Err(err) = ctx.history.save_session(session_name, &messages) {
                ctx.error(&format!(
                    "Failed to save session '{}': {:?}",
                    session_name, err
                ));
            }
        }

        if Confirm::with_theme(&ColorfulTheme::default())
            .with_prompt("Write file?")
            .interact()
            .unwrap()
        {
            let mut file = File::create(path).expect("Failed to open file");
            file.write_all(revision.as_bytes())
                .expect("Failed to write file");
            ctx.success("File written!");
        } else {
            ctx.warn("You chose not to write the file. Give more input to revise.");
        }
    }
}
