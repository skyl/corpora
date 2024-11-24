use serde_json::{self};
use std::fs::{self, File};
use std::io::{self};
use std::path::PathBuf;

use crate::history::ChatHistory;
use corpora_client::models::MessageSchema;

pub struct FileChatHistory {
    directory: PathBuf,
}

impl FileChatHistory {
    pub fn new(directory: PathBuf) -> Self {
        fs::create_dir_all(&directory).expect("Failed to create directory for chat sessions");
        Self { directory }
    }

    fn session_file_path(&self, session_name: &str) -> PathBuf {
        self.directory.join(format!("{}.json", session_name))
    }
}

impl ChatHistory for FileChatHistory {
    fn save_session(&self, session_name: &str, messages: &[MessageSchema]) -> io::Result<()> {
        let file_path = self.session_file_path(session_name);
        let file = File::create(file_path)?;
        serde_json::to_writer(file, messages)?;
        Ok(())
    }

    fn load_session(&self, session_name: &str) -> io::Result<Vec<MessageSchema>> {
        let file_path = self.session_file_path(session_name);
        let file = File::open(file_path)?;
        let messages: Vec<MessageSchema> = serde_json::from_reader(file)?;
        Ok(messages)
    }

    fn list_sessions(&self) -> io::Result<Vec<String>> {
        let mut sessions = Vec::new();
        for entry in fs::read_dir(&self.directory)? {
            let entry_path = entry?.path();
            if let Some(filename) = entry_path.file_name().and_then(|os_str| os_str.to_str()) {
                if let Some(session_name) = filename.strip_suffix(".json") {
                    sessions.push(session_name.to_string());
                }
            }
        }
        Ok(sessions)
    }
}
