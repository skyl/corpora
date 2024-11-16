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
pub struct CorpusUpdateFilesSchema {
    #[serde(
        rename = "delete_files",
        default,
        with = "::serde_with::rust::double_option",
        skip_serializing_if = "Option::is_none"
    )]
    pub delete_files: Option<Option<Vec<String>>>,
}

impl CorpusUpdateFilesSchema {
    pub fn new() -> CorpusUpdateFilesSchema {
        CorpusUpdateFilesSchema { delete_files: None }
    }
}
