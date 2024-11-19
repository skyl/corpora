use serde::{Deserialize, Serialize};
use std::{fs, path::PathBuf};

#[derive(Serialize, Deserialize, Debug)]
pub struct ServerConfig {
    pub base_url: String,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct CorporaConfig {
    pub name: String,
    pub server: ServerConfig,
    pub url: String,

    #[serde(skip)]
    pub root_path: PathBuf,
    #[serde(skip)]
    pub relative_path: String,
    #[serde(skip)]
    pub id: Option<String>,
}

pub fn load_config() -> Option<CorporaConfig> {
    let mut current_dir = std::env::current_dir().ok()?;
    loop {
        let config_path = current_dir.join(".corpora.yaml");
        if config_path.exists() {
            // Read and parse the .corpora.yaml file
            let contents = fs::read_to_string(&config_path).ok()?;
            let mut config: CorporaConfig = serde_yaml::from_str(&contents).ok()?;

            // Add the root_path field
            config.root_path = current_dir.clone();
            config.relative_path = current_dir
                .strip_prefix(&config.root_path) // Borrow config.root_path
                .ok()?
                .to_string_lossy()
                .to_string();

            // Check if the `.corpora/.id` file exists and read its content
            let id_file_path = current_dir.join(".corpora/.id");
            if id_file_path.exists() {
                if let Ok(id_content) = fs::read_to_string(&id_file_path) {
                    config.id = Some(id_content.trim().to_string());
                }
            } else {
                config.id = None;
            }

            return Some(config);
        }

        // Move to the parent directory
        if !current_dir.pop() {
            break;
        }
    }
    None
}
