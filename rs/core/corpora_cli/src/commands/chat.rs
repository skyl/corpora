use crate::context::Context;
use clap::Args;
use corpora_client::models::{CorpusChatSchema, MessageSchema};
use std::fs;
use termimad::MadSkin;

#[derive(Args)]
pub struct ChatArgs {
    #[arg(short, long, help = "name of persistent session")]
    pub persist: Option<String>,
    #[arg(short, long, help = "list available sessions")]
    pub list: bool,
}

/// Executes the chat command operation
pub fn run(ctx: &Context, args: ChatArgs) {
    // If the `--list` flag is provided, list available sessions and exit
    if args.list {
        let sessions = ctx
            .history
            .list_sessions()
            .expect("Failed to list sessions");
        ctx.success("Available sessions:");
        for session in sessions {
            ctx.dim(&session);
        }
        return;
    }

    // Initialize messages
    let mut messages = if let Some(session_name) = &args.persist {
        // Try to load the session if `--persist` is provided
        match ctx.history.load_session(session_name) {
            Ok(existing_messages) => {
                ctx.success(&format!("Loaded session: {}", session_name));
                for message in &existing_messages {
                    ctx.dim(&format!("{}: {}", message.role, message.text));
                }
                existing_messages
            }
            Err(_) => {
                ctx.warn(&format!("No existing session found for: {}", session_name));
                Vec::new()
            }
        }
    } else {
        // No `--persist`, start a new session
        ctx.dim("No persistence specified. Starting a new session.");
        Vec::new()
    };

    loop {
        ctx.magenta("Opening editor for user input...");
        let user_input = ctx
            .get_user_input_via_editor("")
            .expect("Failed to obtain user input");

        // Add the user's input to the chat history
        messages.push(MessageSchema {
            role: "user".to_string(),
            text: user_input.trim().to_string(),
        });

        ctx.success("Thinking...");
        let root_path = &ctx.corpora_config.root_path;
        let voice = fs::read_to_string(root_path.join(".corpora/VOICE.md")).unwrap_or_default();
        let purpose = fs::read_to_string(root_path.join(".corpora/PURPOSE.md")).unwrap_or_default();
        let structure =
            fs::read_to_string(root_path.join(".corpora/STRUCTURE.md")).unwrap_or_default();

        match corpora_client::apis::corpus_api::chat(
            &ctx.api_config,
            CorpusChatSchema {
                messages: messages.clone(),
                corpus_id: ctx
                    .corpora_config
                    .id
                    .clone()
                    .expect("Failed to get corpus ID"),
                voice: Some(voice),
                purpose: Some(purpose),
                structure: Some(structure),
                directions: None,
            },
        ) {
            Ok(response) => {
                let skin = MadSkin::default();
                skin.print_text(&response);
                messages.push(MessageSchema {
                    role: "assistant".to_string(),
                    text: response.clone(),
                });

                // Conditionally save the session if `--persist` is provided
                if let Some(session_name) = &args.persist {
                    if let Err(err) = ctx.history.save_session(session_name, &messages) {
                        ctx.error(&format!(
                            "Failed to save session '{}': {:?}",
                            session_name, err
                        ));
                    }
                }
            }
            Err(err) => {
                ctx.error(&format!("Failed to get response: {:?}", err));
                continue;
            }
        };
    }
}
