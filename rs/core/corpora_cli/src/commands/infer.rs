use crate::context::Context;
use clap::Args;
use corpora_client::models::{CorpusFileChatSchema, MessageSchema};
use std::fs::{self, File};
use std::io::Write;
use std::path::Path;
use std::process::{Command, Stdio};

const MAX_RETRIES: u8 = 2;

#[derive(Args)]
pub struct InferArgs {
    #[arg(help = "Path to the file")]
    pub path: String,

    #[arg(short, long, help = "Check script to validate the output")]
    pub check: Option<String>,

    #[arg(short, long, help = "Instructions for the AI")]
    pub instructions: Option<String>,
}

/// Read existing file content or return a default message
fn get_current_file_content(path: &Path) -> String {
    match fs::read_to_string(path) {
        Ok(content) if !content.trim().is_empty() => content,
        // _ => "FILE CURRENTLY EMPTY. PLEASE INFER CONTENT.".to_string(),
        // add file path to message:
        _ => format!(
            "FILE CURRENTLY EMPTY. PLEASE INFER CONTENT FOR `{}`.",
            path.display()
        ),
    }
}

/// The `infer` command: generates or refines a file
pub fn run(ctx: &Context, args: InferArgs) {
    let path = Path::new(&args.path);
    let cwd = std::env::current_dir().expect("Failed to get current directory");
    let absolute_path = cwd.join(path);
    let relative_path = absolute_path
        .strip_prefix(&ctx.corpora_config.root_path)
        .expect("Failed to get relative path");

    ctx.magenta(&format!("Inferring file: {}", relative_path.display()));
    let ext = relative_path
        .extension()
        .and_then(|s| s.to_str())
        .unwrap_or("");

    // Read current file content if it exists
    let current_file_content = get_current_file_content(path);

    // Load metadata
    let root_path = &ctx.corpora_config.root_path;
    let voice = fs::read_to_string(root_path.join(".corpora/VOICE.md")).unwrap_or_default();
    let purpose = fs::read_to_string(root_path.join(".corpora/PURPOSE.md")).unwrap_or_default();
    let structure = fs::read_to_string(root_path.join(".corpora/STRUCTURE.md")).unwrap_or_default();
    let directions = fs::read_to_string(root_path.join(format!(".corpora/{}/DIRECTIONS.md", ext)))
        .unwrap_or_default();

    let mut attempts = 0;
    let mut previous_error_message = None;

    loop {
        // Send to inference API (no user input)
        ctx.success("Generating file content...");

        let mut messages = vec![MessageSchema {
            role: "user".to_string(),
            // Use the current file content and the instructions provided by the user
            // text: current_file_content.clone(),
            text: format!(
                "{}\n\n{}",
                current_file_content,
                args.instructions
                    .clone()
                    .unwrap_or_else(|| { "".to_string() })
            ),
        }];

        // If previous attempt failed, add error details to AI request
        if let Some(error_msg) = &previous_error_message {
            messages.push(MessageSchema {
                role: "user".to_string(),
                text: format!(
                    "Previous attempt failed. Here is the error output:\n```\n{}\n```\n Please fix the error and try again.",
                    error_msg
                ),
            });
        }

        let inferred_content = match corpora_client::apis::workon_api::file(
            &ctx.api_config,
            CorpusFileChatSchema {
                messages,
                corpus_id: ctx
                    .corpora_config
                    .id
                    .clone()
                    .expect("Failed to get corpus ID"),
                path: relative_path.to_string_lossy().to_string(),
                voice: Some(voice.clone()),
                purpose: Some(purpose.clone()),
                structure: Some(structure.clone()),
                directions: Some(directions.clone()),
            },
        ) {
            Ok(response) => response,
            Err(err) => {
                ctx.error(&format!("Failed to generate content: {:?}", err));
                return;
            }
        };

        ctx.dim(&inferred_content);
        ctx.highlight(&format!("^^Generated for `{}`^^", relative_path.display()));

        // Write file
        let mut file = File::create(path).expect("Failed to open file");
        file.write_all(inferred_content.as_bytes())
            .expect("Failed to write file");
        ctx.success("File written!");

        // Run user-specified check, if any
        if let Some(check_cmd) = &args.check {
            match check_file(ctx, check_cmd) {
                Ok(_) => {
                    ctx.success("Check passed. File is complete!");
                    break; // Exit loop if everything is successful
                }
                Err(error_output) => {
                    ctx.warn("Check failed. Retrying with error context...");

                    previous_error_message = Some(error_output.clone());
                    attempts += 1;

                    if attempts >= MAX_RETRIES {
                        ctx.error("Max retries reached. Aborting.");
                        std::process::exit(1);
                    }
                    continue; // Retry with new AI request including error output
                }
            }
        } else {
            break; // No check provided, exit
        }
    }
}

/// Run an arbitrary check script and capture its output
fn check_file(ctx: &Context, check_cmd: &str) -> Result<(), String> {
    ctx.magenta(&format!("Running check: {}", check_cmd));

    let output = Command::new("sh")
        .arg("-c")
        .arg(check_cmd)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .output()
        .expect("Failed to run check");

    if output.status.success() {
        Ok(())
    } else {
        // debug print error
        println!("{:?}", output);

        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);
        let error_message = format!(
            "Check `{}` failed.\nSTDOUT:\n{}\nSTDERR:\n{}",
            check_cmd, stdout, stderr
        );
        Err(error_message)
    }
}
