use crate::context::Context;
use base64::Engine;
use clap::Args;
use corpora_client::models::{CorpusChatSchema, MessageSchema};
use std::fs::File;
use std::io::Write;
use std::path::Path;
use std::process::{Command, Stdio};

const MAX_RETRIES: u8 = 2;

#[derive(Args)]
pub struct PlotArgs {
    #[arg(help = "Natural language description of the plot (e.g., 'plot x squared')")]
    pub description: String,

    #[arg(short, long, help = "Output path for the PNG file")]
    pub output: String,

    #[arg(short, long, help = "Check script to validate the output")]
    pub check: Option<String>,
}

/// The `plot` command: generates a Matplotlib plot and saves it as a PNG
pub fn run(ctx: &Context, args: PlotArgs) {
    let output_path = Path::new(&args.output);
    let cwd = std::env::current_dir().expect("Failed to get current directory");
    let absolute_path = cwd.join(output_path);
    let relative_path = absolute_path
        .strip_prefix(&ctx.corpora_config.root_path)
        .expect("Failed to get relative path");

    ctx.magenta(&format!("Generating plot: {}", relative_path.display()));

    // Load metadata (consistent with infer command)
    let root_path = &ctx.corpora_config.root_path;
    let voice = std::fs::read_to_string(root_path.join(".corpora/VOICE.md")).unwrap_or_default();
    let purpose =
        std::fs::read_to_string(root_path.join(".corpora/PURPOSE.md")).unwrap_or_default();
    // TODO: ... these could be optional in the struct but then passed via command line?
    let structure: String =
        "A professional plot, well though out in terms of labels and ranges".to_string();
    let directions: String = "Produce a perfect plot for a college algebra textbook".to_string();

    let mut attempts = 0;
    let mut previous_error_message = None;

    loop {
        ctx.success("Generating plot...");

        // Prepare messages for the API
        let mut messages = vec![MessageSchema {
            role: "user".to_string(),
            text: format!(
                "{}\n\n{}",
                args.description,
                previous_error_message
                    .as_ref()
                    .map(|_| "Please ensure the plot is valid and meets requirements.")
                    .unwrap_or("")
            ),
        }];

        // If previous attempt failed, add error details
        if let Some(error_msg) = &previous_error_message {
            messages.push(MessageSchema {
                role: "user".to_string(),
                text: format!(
                    "Previous attempt failed. Error output:\n```\n{}\n```\nPlease fix and retry.",
                    error_msg
                ),
            });
        }

        // Call the /api/plots/matplotlib endpoint
        let plot_response = match corpora_client::apis::plots_api::get_matplotlib_plot(
            &ctx.api_config,
            CorpusChatSchema {
                messages,
                corpus_id: ctx
                    .corpora_config
                    .id
                    .clone()
                    .expect("Failed to get corpus ID"),
                voice: Some(voice.clone()),
                purpose: Some(purpose.clone()),
                structure: Some(structure.clone()),
                directions: Some(directions.clone()),
            },
        ) {
            Ok(response) => response,
            Err(err) => {
                ctx.error(&format!("Failed to generate plot: {:?}", err));
                return;
            }
        };

        // Decode base64 PNG
        let mut png_bytes = Vec::new();
        match base64::engine::general_purpose::STANDARD
            .decode_vec(&plot_response.plot, &mut png_bytes)
        {
            Ok(_) => (),
            Err(err) => {
                ctx.error(&format!("Failed to decode PNG: {:?}", err));
                return;
            }
        };

        // Write PNG to file
        let mut file = match File::create(&output_path) {
            Ok(file) => file,
            Err(err) => {
                ctx.error(&format!("Failed to create file: {:?}", err));
                return;
            }
        };
        if let Err(err) = file.write_all(&png_bytes) {
            ctx.error(&format!("Failed to write PNG: {:?}", err));
            return;
        }
        ctx.success(&format!("Plot saved to {}", relative_path.display()));

        // Run user-specified check, if any
        if let Some(check_cmd) = &args.check {
            match check_file(ctx, check_cmd) {
                Ok(_) => {
                    ctx.success("Check passed. Plot is complete!");
                    break;
                }
                Err(error_output) => {
                    ctx.warn("Check failed. Retrying with error context...");
                    previous_error_message = Some(error_output);
                    attempts += 1;

                    if attempts >= MAX_RETRIES {
                        ctx.error("Max retries reached. Aborting.");
                        std::process::exit(1);
                    }
                    continue;
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
        let stdout = String::from_utf8_lossy(&output.stdout);
        let stderr = String::from_utf8_lossy(&output.stderr);
        let error_message = format!(
            "Check `{}` failed.\nSTDOUT:\n{}\nSTDERR:\n{}",
            check_cmd, stdout, stderr
        );
        Err(error_message)
    }
}
