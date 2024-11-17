use clap::Args;

/// Arguments for the `update` subcommand
#[derive(Args)]
pub struct UpdateArgs {
    #[arg(help = "ID of the issue to update")]
    pub id: u32,
}

/// Run the `update` subcommand
pub fn run(args: UpdateArgs) {
    println!("Updating issue with ID: {}", args.id);
}
