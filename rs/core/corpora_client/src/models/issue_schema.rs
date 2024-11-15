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
pub struct IssueSchema {
    #[serde(rename = "title")]
    pub title: String,
    #[serde(rename = "body")]
    pub body: String,
}

impl IssueSchema {
    pub fn new(title: String, body: String) -> IssueSchema {
        IssueSchema {
            title,
            body,
        }
    }
}

