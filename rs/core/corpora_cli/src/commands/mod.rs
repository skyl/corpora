pub mod chat;
pub mod init;
pub mod issue;
pub mod sync;
pub mod workon;

use clap::Subcommand;

/// Define all top-level subcommands for the CLI
#[derive(Subcommand)]
pub enum Commands {
    #[command(about = "Initial setup and uploads to the server")]
    Init,
    #[command(about = "Chat the corpus")]
    Chat(chat::ChatArgs),
    #[command(about = "Find the diff and sync changes to the server")]
    Sync,
    #[command(about = "Work on a specific file")]
    Workon(workon::WorkonArgs),
    #[command(about = "Manage issues", subcommand)]
    Issue(issue::IssueCommands),
}
