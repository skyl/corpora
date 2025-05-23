pub mod chat;
pub mod infer;
pub mod init;
pub mod issue;
pub mod plot;
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
    Sync(sync::SyncArgs),
    #[command(about = "Work on a specific file")]
    Workon(workon::WorkonArgs),
    #[command(about = "Infer a file")]
    Infer(infer::InferArgs),
    #[command(about = "Manage issues", subcommand)]
    Issue(issue::IssueCommands),
    #[command(about = "Generate a plot")]
    Plot(plot::PlotArgs),
}
