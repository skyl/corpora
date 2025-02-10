pub mod auth;
pub mod collector;
pub mod config;

use std::fs;
use std::sync::Arc;
use std::time::Duration;
use std::{env, process::Command};

use console::{Style, Term};
use indicatif::{ProgressBar, ProgressStyle};
use reqwest::blocking::ClientBuilder;
use tempfile::NamedTempFile;

use crate::history::files::FileChatHistory;
use crate::history::ChatHistory;
use corpora_client::apis::configuration::Configuration;

use auth::get_bearer_token;
use collector::{get_collector, Collector};
use config::{load_config, CorporaConfig};

pub struct Context {
    pub api_config: Configuration,
    pub corpora_config: CorporaConfig,
    pub collector: Box<dyn Collector>,
    pub term: Arc<Term>,
    pub history: Box<dyn ChatHistory>,
}

impl Context {
    pub fn new() -> Self {
        let corpora_config = load_config().expect("Failed to load Corpora configuration");
        let token = get_bearer_token(&corpora_config)
            .expect("Failed to authenticate and retrieve bearer token");
        let client = ClientBuilder::new()
            .timeout(Duration::from_secs(60))
            .build()
            .expect("Failed to build the reqwest client");
        let api_config = Configuration {
            base_path: corpora_config.server.base_url.clone(),
            client,
            bearer_access_token: Some(token),
            ..Default::default()
        };
        let collector =
            get_collector(&corpora_config).expect("Failed to initialize a file collector");
        let term = Arc::new(Term::stdout());
        let history = FileChatHistory::new(corpora_config.root_path.join(".corpora/chat"));

        Context {
            api_config,
            corpora_config,
            collector,
            term,
            history: Box::new(history),
        }
    }

    pub fn print(&self, message: &str, style: Style) {
        let styled_message = style.apply_to(message);
        self.term.write_line(&styled_message.to_string()).unwrap();
    }

    pub fn prompt_confirm(&self, prompt: &str) -> bool {
        dialoguer::Confirm::new()
            .default(false)
            .with_prompt(prompt)
            .interact()
            .unwrap_or_else(|_| {
                eprintln!("Failed to get user confirmation");
                std::process::exit(1);
            })
    }

    pub fn progress_bar(&self, length: u64, message: &str) -> ProgressBar {
        let bar = ProgressBar::new(length);
        bar.set_style(
            ProgressStyle::default_bar()
                .template("{spinner:.green} [{elapsed}] {bar:40.cyan/blue} {pos}/{len} {msg}")
                .unwrap()
                .progress_chars("=>-"),
        );
        bar.set_message(message.to_string());
        bar
    }

    pub fn success(&self, message: &str) {
        self.print(message, Style::new().green().bold());
    }

    pub fn error(&self, message: &str) {
        self.print(message, Style::new().red().bold());
    }

    pub fn warn(&self, message: &str) {
        self.print(message, Style::new().yellow().bold());
    }

    pub fn dim(&self, message: &str) {
        self.print(message, Style::new().dim());
    }

    pub fn magenta(&self, message: &str) {
        self.print(message, Style::new().magenta());
    }

    pub fn highlight(&self, message: &str) {
        self.print(message, Style::new().bold().green().on_magenta());
    }

    pub fn get_user_input_via_editor(&self, initial_content: &str) -> Result<String, String> {
        get_user_input_via_editor(initial_content)
    }
}

pub fn get_user_input_via_editor(initial_content: &str) -> Result<String, String> {
    let temp_file =
        NamedTempFile::new().map_err(|e| format!("Failed to create temp file: {}", e))?;
    fs::write(temp_file.path(), initial_content)
        .map_err(|e| format!("Failed to write to temp file: {}", e))?;
    let editor = env::var("EDITOR").unwrap_or_else(|_| detect_default_editor());

    println!("DEBUG: Using editor: {}", editor);

    let mut command = Command::new(&editor);
    if editor == "code" || editor == "subl" {
        command.arg("--wait"); // Append --wait conditionally
    }
    let status = command
        .arg(temp_file.path()) // Always pass the file path separately
        .status()
        .map_err(|e| {
            format!(
                "Failed to launch editor '{} {}': {}",
                editor,
                temp_file.path().display(),
                e
            )
        })?;

    if !status.success() {
        return Err(format!("Editor '{}' exited with a non-zero status", editor));
    }
    fs::read_to_string(temp_file.path()).map_err(|e| format!("Failed to read edited file: {}", e))
}

fn detect_default_editor() -> String {
    if env::var("VSCODE_PID").is_ok() || env::var("VSCODE_IPC_HOOK_CLI").is_ok() {
        return "code".to_string(); // No more hardcoded path!
    }
    let editors = ["nano", "vim", "vi", "subl", "gedit", "notepad"];
    for editor in editors {
        if is_command_available(editor.split_whitespace().next().unwrap()) {
            return editor.to_string();
        }
    }
    "nano".to_string()
}

fn is_command_available(cmd: &str) -> bool {
    Command::new("which")
        .arg(cmd)
        .status()
        .is_ok_and(|s| s.success())
}
