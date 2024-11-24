pub mod files;
use corpora_client::models::MessageSchema;

pub trait ChatHistory {
    fn save_session(&self, session_name: &str, messages: &[MessageSchema]) -> std::io::Result<()>;
    fn load_session(&self, session_name: &str) -> std::io::Result<Vec<MessageSchema>>;
    fn list_sessions(&self) -> std::io::Result<Vec<String>>;
}
