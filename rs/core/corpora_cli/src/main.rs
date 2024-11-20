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
        // TODO: Unify All Commands to Return Result
        // Modify the run functions for all commands (init, sync, etc.)
        // to return Result<(), std::io::Error>.
        // This aligns with idiomatic Rust practices
        // where errors are propagated explicitly.
        Commands::Chat => {
            if let Err(err) = commands::chat::run(&ctx) {
                eprintln!("Error in chat command: {}", err);
            }
        }
        Commands::Workon(args) => commands::workon::run(&ctx, args),
        Commands::Issue(issue_command) => match issue_command {
            issue::IssueCommands::Create => issue::create(&ctx),
            issue::IssueCommands::Update(args) => issue::update(&ctx, args),
            issue::IssueCommands::Label(args) => issue::label(&ctx, args),
        },
    }
}
