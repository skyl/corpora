mod commands;

use clap::Parser;
use commands::{issue, Commands};

/// The main CLI app definition
#[derive(Parser)]
#[command(
    name = "Corpora CLI",
    about = "Manage and process your corpora",
    version = "0.1.0",
    author = "Your Name"
)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

fn main() {
    let cli = Cli::parse();

    match cli.command {
        Commands::Init => commands::init::run(),
        Commands::Sync => commands::sync::run(),
        Commands::Workon(args) => commands::workon::run(args),
        Commands::Issue(issue_command) => match issue_command {
            issue::IssueCommands::Create => issue::create(),
            issue::IssueCommands::Update(args) => issue::update(args),
            issue::IssueCommands::Label(args) => issue::label(args),
        },
    }
}
