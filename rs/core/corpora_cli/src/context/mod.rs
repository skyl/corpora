pub mod auth;
pub mod collector;
pub mod config;

use auth::get_bearer_token;
use collector::{get_collector, Collector};
use config::{load_config, CorporaConfig};
use corpora_client::apis::configuration::Configuration;

pub struct Context {
    pub api_config: Configuration,
    pub corpora_config: CorporaConfig,
    pub collector: Box<dyn Collector>,
}

impl Context {
    /// Initialize a new context with configuration, authentication, and a file collector
    pub fn new() -> Self {
        // Load the Corpora configuration
        let corpora_config = load_config().expect("Failed to load Corpora configuration");

        // Authenticate and get a bearer token
        let token = get_bearer_token(&corpora_config)
            .expect("Failed to authenticate and retrieve bearer token");

        // Configure the API client
        let api_config = Configuration {
            base_path: corpora_config.server.base_url.clone(),
            bearer_access_token: Some(token),
            ..Default::default()
        };

        // Get the appropriate file collector (e.g., GitCollector)
        let collector =
            get_collector(&corpora_config).expect("Failed to initialize a file collector");

        Context {
            api_config,
            corpora_config,
            collector,
        }
    }
}
