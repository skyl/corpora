pub mod auth;
pub mod collector;
pub mod config;

use console::{Style, Term};
use indicatif::{ProgressBar, ProgressStyle};
use std::sync::Arc;

use corpora_client::apis::configuration::Configuration;

use auth::get_bearer_token;
use collector::{get_collector, Collector};
use config::{load_config, CorporaConfig};

pub struct Context {
    pub api_config: Configuration,
    pub corpora_config: CorporaConfig,
    pub collector: Box<dyn Collector>,
    pub term: Arc<Term>, // Terminal for colorful and interactive output
}

impl Context {
    /// Initialize a new context with configuration, authentication, and a file collector
    pub fn new() -> Self {
        // Load the Corpora configuration
        let corpora_config = load_config().expect("Failed to load Corpora configuration");

        // Authenticate and get a bearer token
        let token = get_bearer_token(&corpora_config)
            .expect("Failed to authenticate and retrieve bearer token");

        // Configure the API client
        let api_config = Configuration {
            base_path: corpora_config.server.base_url.clone(),
            bearer_access_token: Some(token),
            ..Default::default()
        };

        // Get the appropriate file collector (e.g., GitCollector)
        let collector =
            get_collector(&corpora_config).expect("Failed to initialize a file collector");

        // Create terminal instance for interactive output
        let term = Arc::new(Term::stdout());

        Context {
            api_config,
            corpora_config,
            collector,
            term,
        }
    }

    /// Print a styled message to the terminal
    ///
    /// # Arguments
    /// * `message` - The message to print.
    /// * `style` - The style to apply to the message.
    pub fn print(&self, message: &str, style: Style) {
        let styled_message = style.apply_to(message);
        self.term.write_line(&styled_message.to_string()).unwrap();
    }

    // /// Prompt the user for input using dialoguer
    // ///
    // /// # Arguments
    // /// * `prompt` - The message to display as a prompt.
    // ///
    // /// # Returns
    // /// The user's input as a `String`.
    // pub fn prompt(&self, prompt: &str) -> String {
    //     dialoguer::Input::new()
    //         .with_prompt(prompt)
    //         .interact_text()
    //         .unwrap_or_else(|_| {
    //             eprintln!("Failed to get user input");
    //             std::process::exit(1);
    //         })
    // }

    /// Prompt the user for confirmation using dialoguer
    /// The user must type 'y' or 'yes' to confirm.
    /// Returns true if the user confirms, false otherwise.
    /// # Arguments
    /// * `prompt` - The message to display as a prompt.
    /// # Returns
    /// A boolean indicating whether the user confirmed.
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

    /// Display a progress bar
    ///
    /// # Arguments
    /// * `length` - The total number of steps for the progress bar.
    /// * `message` - The message to display alongside the progress bar.
    ///
    /// # Returns
    /// A `ProgressBar` instance.
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

    /// Print a success message
    ///
    /// # Arguments
    /// * `message` - The message to print.
    pub fn success(&self, message: &str) {
        let success_style = Style::new().green().bold();
        self.print(message, success_style);
    }

    /// Print an error message
    ///
    /// # Arguments
    /// * `message` - The error message to print.
    pub fn error(&self, message: &str) {
        let error_style = Style::new().red().bold();
        self.print(message, error_style);
    }

    /// Print a warning message
    ///
    /// # Arguments
    /// * `message` - The warning message to print.
    pub fn warn(&self, message: &str) {
        let warn_style = Style::new().yellow().bold();
        self.print(message, warn_style);
    }

    /// Print a dim message
    /// Dim messages are used for less important information
    /// # Arguments
    /// * `message` - The message to print.
    pub fn dim(&self, message: &str) {
        let dim_style = Style::new().dim();
        self.print(message, dim_style);
    }
}
