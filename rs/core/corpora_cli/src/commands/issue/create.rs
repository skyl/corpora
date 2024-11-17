use crate::context::Context;
/// Run the `create` subcommand
pub fn run(ctx: &Context) {
    println!("Creating issue");
    println!("Server URL: {}", ctx.config.base_path);
}
