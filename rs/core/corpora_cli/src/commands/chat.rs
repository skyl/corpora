use crate::context::Context;
use corpora_client::models::{CorpusChatSchema, MessageSchema};
use std::fs;
use termimad::MadSkin;

/// The `workon` command operation
pub fn run(ctx: &Context) {
    let mut messages: Vec<MessageSchema> = Vec::new();

    // REPL loop
    loop {
        // // TODO: multiline input
        // let user_input: String = Input::with_theme(&ColorfulTheme::default())
        //     .with_prompt("Can I help you?")
        //     .allow_empty(false)
        //     .interact_text()
        //     .unwrap();
        let user_input = ctx
            .get_user_input_via_editor("Put your prompt here and close")
            .expect("FML");
        // Add the user's input as a new message
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

        // println!("Voice: {}", voice);
        // println!("Purpose: {}", purpose);
        // println!("Structure: {}", structure);

        let response = match corpora_client::apis::corpus_api::chat(
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
            Ok(response) => response,
            Err(err) => {
                ctx.error(&format!("Failed to get response: {:?}", err));
                continue;
            }
        };

        // ctx.print(&response, dialoguer::console::Style::new().dim());
        let skin = MadSkin::default();
        skin.print_text(&response);

        // println!("{}", relative_path.display());
        messages.push(MessageSchema {
            role: "assistant".to_string(),
            text: response.clone(),
        });
    }
}
