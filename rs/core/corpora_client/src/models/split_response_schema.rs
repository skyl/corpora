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
pub struct SplitResponseSchema {
    #[serde(rename = "id")]
    pub id: uuid::Uuid,
    #[serde(rename = "content")]
    pub content: String,
    #[serde(rename = "order")]
    pub order: i32,
    #[serde(rename = "file_id")]
    pub file_id: uuid::Uuid,
}

impl SplitResponseSchema {
    pub fn new(id: uuid::Uuid, content: String, order: i32, file_id: uuid::Uuid) -> SplitResponseSchema {
        SplitResponseSchema {
            id,
            content,
            order,
            file_id,
        }
    }
}

