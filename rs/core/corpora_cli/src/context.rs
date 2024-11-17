use corpora_client::apis::configuration::Configuration;
use serde::{Deserialize, Serialize};
use std::{env, fs};

#[derive(Serialize, Deserialize, Debug)]
pub struct ServerConfig {
    pub base_url: String,
}

#[derive(Serialize, Deserialize, Debug)]
/// Configuration from a .corpora.yaml file
pub struct CorporaConfig {
    pub name: String,
    pub server: ServerConfig,
    pub url: String,
}

pub struct Context {
    pub api_config: Configuration,
    pub corpora_config: CorporaConfig,
}

impl Context {
    /// Initialize a new context with OAuth authentication and configuration
    pub fn new() -> Self {
        // Derive name and URL from `.corpora.yaml` or Git
        let (name, url) = match Self::find_corpora_config() {
            Some(config) => (config.name, config.url),
            None => {
                eprintln!("Could not find `.corpora.yaml`. Falling back to Git-derived values...");
                Self::from_git_repo().unwrap_or_else(|| {
                    panic!("This is not a Git repository and `.corpora.yaml` is missing.")
                })
            }
        };

        // Get server.base_url from .corpora.yaml or use default
        let server_base_url =
            Self::get_server_base_url().unwrap_or_else(|| "http://app:8877".to_string());

        let corpora_config = CorporaConfig {
            name,
            server: ServerConfig {
                base_url: server_base_url.clone(),
            },
            url,
        };

        // Fetch client ID and secret from environment variables
        let client_id = env::var("CORPORA_CLIENT_ID")
            .expect("Environment variable CORPORA_CLIENT_ID is not set");
        let client_secret = env::var("CORPORA_CLIENT_SECRET")
            .expect("Environment variable CORPORA_CLIENT_SECRET is not set");

        // Perform OAuth authentication to fetch a bearer token
        let bearer_access_token =
            Self::get_oauth_token(&client_id, &client_secret, &server_base_url);

        // Configure the client using a struct literal
        let api_config = Configuration {
            base_path: server_base_url,
            bearer_access_token: Some(bearer_access_token),
            ..Default::default()
        };

        Context {
            api_config,
            corpora_config,
        }
    }

    /// Search for `.corpora.yaml` in the current directory or its parents
    fn find_corpora_config() -> Option<CorporaConfig> {
        let mut current_dir = std::env::current_dir().ok()?;
        loop {
            let config_path = current_dir.join(".corpora.yaml");
            if config_path.exists() {
                let contents = fs::read_to_string(&config_path).ok()?;
                return serde_yaml::from_str(&contents).ok();
            }

            // Move to the parent directory
            if !current_dir.pop() {
                break; // We've reached the filesystem root
            }
        }
        None
    }

    /// Derive `name` and `url` from a Git repository
    fn from_git_repo() -> Option<(String, String)> {
        let repo = git2::Repository::discover(".").ok()?;
        let remote = repo.find_remote("origin").ok()?;
        let remote_url = remote.url()?.to_string();

        // Derive the name and URL
        let name = remote_url
            .split('/')
            .last()
            .unwrap_or_default()
            .trim_end_matches(".git")
            .to_string();

        Some((name, remote_url))
    }

    /// Get `server.base_url` from `.corpora.yaml` or return `None`
    fn get_server_base_url() -> Option<String> {
        Self::find_corpora_config().map(|config| config.server.base_url)
    }

    /// Perform OAuth authentication and fetch a bearer token
    fn get_oauth_token(client_id: &str, client_secret: &str, server_url: &str) -> String {
        let token_url = format!("{}/o/token/", server_url);

        let client = reqwest::blocking::Client::new();
        let response = client
            .post(&token_url)
            .form(&[
                ("grant_type", "client_credentials"),
                ("client_id", client_id),
                ("client_secret", client_secret),
            ])
            .send()
            .expect("Failed to perform OAuth authentication");

        if !response.status().is_success() {
            panic!(
                "Failed to fetch OAuth token: {}",
                response.text().unwrap_or_default()
            );
        }

        let token_response: serde_json::Value = response
            .json()
            .expect("Failed to parse OAuth token response as JSON");

        token_response["access_token"]
            .as_str()
            .expect("Access token not found in OAuth response")
            .to_string()
    }
}
