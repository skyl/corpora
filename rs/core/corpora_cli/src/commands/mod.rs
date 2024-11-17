pub mod init;
pub mod sync;
pub mod workon;

use clap::Subcommand;

/// Define all subcommands for the CLI
#[derive(Subcommand)]
pub enum Commands {
    Init,
    Sync,
    Workon(workon::WorkonArgs),
}
