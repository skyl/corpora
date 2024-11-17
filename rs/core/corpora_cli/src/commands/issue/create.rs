use clap::Args;

/// Arguments for the `create` subcommand
#[derive(Args)]
pub struct CreateArgs {
    #[arg(help = "Title of the issue")]
    pub title: String,
}

/// Run the `create` subcommand
pub fn run(args: CreateArgs) {
    println!("Creating issue with title: {}", args.title);
}
