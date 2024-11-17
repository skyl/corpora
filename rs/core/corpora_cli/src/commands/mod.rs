pub mod corpus;

use clap::Subcommand;

/// Define all subcommands for the CLI
#[derive(Subcommand)]
pub enum Commands {
    /// Manage corpora
    Corpus(corpus::CorpusArgs),
}
