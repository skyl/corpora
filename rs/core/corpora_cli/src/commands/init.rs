use crate::context::Context;

pub fn run(ctx: &Context) {
    println!("Initializing a new corpus...");

    let corpus_name = "example_corpus";
    let tarball_path = std::path::PathBuf::from("path/to/tarball.tar");

    match corpora_client::apis::corpus_api::create_corpus(
        &ctx.config,
        corpus_name,
        tarball_path,
        None,
    ) {
        Ok(response) => {
            println!("Corpus created successfully: {:?}", response);
        }
        Err(err) => {
            eprintln!("Failed to create corpus: {:?}", err);
        }
    }
}
