pub mod client_secret;

use crate::context::config::CorporaConfig;
use client_secret::ClientSecretAuth;

/// Defines a trait for authentication strategies
pub trait AuthStrategy {
    /// Performs authentication and returns a bearer token
    fn authenticate(&self) -> Result<String, AuthError>;
}

/// Enum representing different types of authentication errors
#[derive(Debug)]
#[allow(dead_code)]
pub enum AuthError {
    MissingEnvironmentVariables(String),
    AuthenticationFailed(String),
    NotImplemented(String),
}

/// Selects the appropriate authentication strategy and retrieves a bearer token
///
/// # Arguments
/// * `config` - The `CorporaConfig` containing the server base URL.
///
/// # Returns
/// A `Result` containing the bearer token or an `AuthError`.
pub fn get_bearer_token(config: &CorporaConfig) -> Result<String, AuthError> {
    // Determine if ClientSecretAuth is applicable based on environment variables
    if let Ok(client_id) = std::env::var("CORPORA_CLIENT_ID") {
        let client_secret = std::env::var("CORPORA_CLIENT_SECRET").map_err(|_| {
            AuthError::MissingEnvironmentVariables("CORPORA_CLIENT_SECRET is missing".into())
        })?;
        let client_secret_auth =
            ClientSecretAuth::new(&config.server.base_url, &client_id, &client_secret);
        return client_secret_auth.authenticate();
    }

    // If no valid strategy is found, return an error
    Err(AuthError::NotImplemented(
        "No valid authentication strategy found.".to_string(),
    ))
}
