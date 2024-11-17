use clap::Args;

/// Arguments for the `workon` subcommand
#[derive(Args)]
pub struct WorkonArgs {
    /// The path to work on
    #[arg(help = "Path to the file or directory")]
    pub path: String,
}

/// Run the `workon` command
pub fn run(args: WorkonArgs) {
    println!("Workon command executed with path: {}", args.path);
}
