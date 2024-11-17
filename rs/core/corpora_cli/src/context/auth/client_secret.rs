use crate::context::auth::{AuthError, AuthStrategy};
use reqwest::blocking::Client;

/// Implements the `AuthStrategy` trait for client secret-based authentication
pub struct ClientSecretAuth {
    server_base_url: String,
    client_id: String,
    client_secret: String,
}

impl ClientSecretAuth {
    /// Creates a new `ClientSecretAuth` instance
    ///
    /// # Arguments
    /// * `server_base_url` - The base URL of the server.
    /// * `client_id` - The OAuth client ID.
    /// * `client_secret` - The OAuth client secret.
    pub fn new(server_base_url: &str, client_id: &str, client_secret: &str) -> Self {
        Self {
            server_base_url: server_base_url.to_string(),
            client_id: client_id.to_string(),
            client_secret: client_secret.to_string(),
        }
    }
}

impl AuthStrategy for ClientSecretAuth {
    /// Authenticates using client credentials and returns a bearer token
    fn authenticate(&self) -> Result<String, AuthError> {
        let token_url = format!("{}/o/token/", self.server_base_url);

        let client = Client::new();
        let response = client
            .post(&token_url)
            .form(&[
                ("grant_type", "client_credentials"),
                ("client_id", &self.client_id),
                ("client_secret", &self.client_secret),
            ])
            .send()
            .map_err(|e| AuthError::AuthenticationFailed(format!("HTTP request failed: {}", e)))?;

        let status = response.status(); // Extract the status before consuming the response

        if !status.is_success() {
            let error_text = response
                .text()
                .unwrap_or_else(|_| "Unable to retrieve error details".to_string());
            return Err(AuthError::AuthenticationFailed(format!(
                "Authentication failed with status {}: {}",
                status, error_text
            )));
        }

        let token_response: serde_json::Value = response
            .json()
            .map_err(|e| AuthError::AuthenticationFailed(format!("Failed to parse JSON: {}", e)))?;

        token_response["access_token"]
            .as_str()
            .map(|token| token.to_string())
            .ok_or_else(|| {
                AuthError::AuthenticationFailed("Access token not found in response".to_string())
            })
    }
}
