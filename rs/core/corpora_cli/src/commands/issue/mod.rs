pub mod create;
pub mod label;
pub mod update;

use clap::Subcommand;

/// Define the `issue` subcommands
#[derive(Subcommand)]
pub enum IssueCommands {
    #[command(about = "Create a new issue")]
    Create,
    #[command(about = "Update an existing issue by ID")]
    Update(update::UpdateArgs),
    #[command(about = "Label an existing issue by ID")]
    Label(label::LabelArgs),
}

pub use create::run as create;
pub use label::run as label;
pub use update::run as update;
