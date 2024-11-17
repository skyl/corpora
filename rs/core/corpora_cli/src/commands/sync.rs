use crate::context::Context;

/// Run the `sync` command
pub fn run(ctx: &Context) {
    println!("sync command executed with no arguments.");
    println!("Server URL: {}", ctx.config.base_path);
}
