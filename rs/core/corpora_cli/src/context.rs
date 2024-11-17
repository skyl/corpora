use std::env;

use corpora_client::apis::configuration::Configuration;

pub struct Context {
    pub config: Configuration,
}

impl Context {
    /// Initialize a new context with OAuth authentication and configuration
    pub fn new(server_url: &str) -> Self {
        // Fetch client ID and secret from environment variables
        let client_id = env::var("CORPORA_CLIENT_ID")
            .expect("Environment variable CORPORA_CLIENT_ID is not set");
        let client_secret = env::var("CORPORA_CLIENT_SECRET")
            .expect("Environment variable CORPORA_CLIENT_SECRET is not set");

        // Perform OAuth authentication to fetch a bearer token
        let bearer_access_token = Self::get_oauth_token(&client_id, &client_secret, server_url);

        // Configure the client using a struct literal
        let config = Configuration {
            base_path: server_url.to_string(),
            bearer_access_token: Some(bearer_access_token),
            ..Default::default() // Fill in other fields with their default values
        };

        Context { config }
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
