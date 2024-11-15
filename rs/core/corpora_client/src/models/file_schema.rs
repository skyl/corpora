/*
 * Corpora API
 *
 * API for managing and processing corpora
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 * Generated by: https://openapi-generator.tech
 */

use crate::models;
use serde::{Deserialize, Serialize};

#[derive(Clone, Default, Debug, PartialEq, Serialize, Deserialize)]
pub struct FileSchema {
    #[serde(rename = "path")]
    pub path: String,
    #[serde(rename = "content")]
    pub content: String,
    #[serde(rename = "corpus_id")]
    pub corpus_id: uuid::Uuid,
}

impl FileSchema {
    pub fn new(path: String, content: String, corpus_id: uuid::Uuid) -> FileSchema {
        FileSchema {
            path,
            content,
            corpus_id,
        }
    }
}
