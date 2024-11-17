use crate::context::Context;

pub fn run(ctx: &Context) {
    println!("Initializing a new corpus...");

    let corpus_name = ctx.corpora_config.name.clone();
    // let tarball_path = std::path::PathBuf::from("path/to/tarball.tar");
    // TODO: the tarball should be all text files from `git ls-files`
    // produced dynamically from the git repo.

    match corpora_client::apis::corpus_api::create_corpus(
        &ctx.api_config,
        &corpus_name,
        tarball_buf,
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
