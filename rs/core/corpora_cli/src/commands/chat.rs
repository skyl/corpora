use crate::context::Context;
use corpora_client::models::{CorpusChatSchema, MessageSchema};
use std::fs;
use termimad::MadSkin;

/// Executes the chat command operation
pub fn run(ctx: &Context) {
    let mut messages = Vec::new();

    loop {
        let user_input = ctx
            .get_user_input_via_editor("Put your prompt here and close")
            .expect("Failed to obtain user input");

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
            }
            Err(err) => {
                ctx.error(&format!("Failed to get response: {:?}", err));
                continue;
            }
        };
    }
}
