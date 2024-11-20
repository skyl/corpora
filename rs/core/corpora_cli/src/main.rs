mod commands;
mod context;

use clap::Parser;
use commands::{issue, Commands};
use context::Context;

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
    let ctx = Context::new();

    match cli.command {
        Commands::Init => commands::init::run(&ctx),
        Commands::Sync => commands::sync::run(&ctx),
        Commands::Chat => commands::chat::run(&ctx),
        Commands::Workon(args) => commands::workon::run(&ctx, args),
        Commands::Issue(issue_command) => match issue_command {
            issue::IssueCommands::Create => issue::create(&ctx),
            issue::IssueCommands::Update(args) => issue::update(&ctx, args),
            issue::IssueCommands::Label(args) => issue::label(&ctx, args),
        },
    }
}
