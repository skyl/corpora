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
    /// A list of glob patterns to exclude
    pub exclude_globs: Option<Vec<String>>,

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
            let contents = fs::read_to_string(&config_path).ok()?;
            println!("{}", contents);
            let mut config: CorporaConfig = serde_yaml::from_str(&contents).ok()?;

            // Set additional fields that are not part of the config file
            config.root_path = current_dir.clone();
            config.relative_path = current_dir
                .strip_prefix(&config.root_path)
                .ok()?
                .to_string_lossy()
                .to_string();

            let id_file_path = current_dir.join(".corpora/.id");
            if id_file_path.exists() {
                if let Ok(id_content) = fs::read_to_string(&id_file_path) {
                    config.id = Some(id_content.trim().to_string());
                }
            } else {
                config.id = None;
            }

            println!("{:?}", config);
            return Some(config);
        }

        if !current_dir.pop() {
            break;
        }
    }
    None
}
