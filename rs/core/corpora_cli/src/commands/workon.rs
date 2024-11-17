use clap::Args;

/// The `workon` command arguments
#[derive(Args)]
pub struct WorkonArgs {
    #[arg(help = "Path to the file or directory")]
    pub path: String,
}

/// Run the `workon` command
pub fn run(args: WorkonArgs) {
    println!("Workon command executed with path: {}", args.path);
}
