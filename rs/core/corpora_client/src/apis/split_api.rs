/*
 * Corpora API
 *
 * API for managing and processing corpora
 *
 * The version of the OpenAPI document: 0.1.0
 *
 * Generated by: https://openapi-generator.tech
 */

use std::borrow::Borrow;
#[allow(unused_imports)]
use std::option::Option;
use std::pin::Pin;
use std::sync::Arc;

use futures::Future;
use hyper;
use hyper_util::client::legacy::connect::Connect;

use super::request as __internal_request;
use super::{configuration, Error};
use crate::models;

pub struct SplitApiClient<C: Connect>
where
    C: Clone + std::marker::Send + Sync + 'static,
{
    configuration: Arc<configuration::Configuration<C>>,
}

impl<C: Connect> SplitApiClient<C>
where
    C: Clone + std::marker::Send + Sync,
{
    pub fn new(configuration: Arc<configuration::Configuration<C>>) -> SplitApiClient<C> {
        SplitApiClient { configuration }
    }
}

pub trait SplitApi: Send + Sync {
    fn get_split(
        &self,
        split_id: &str,
    ) -> Pin<Box<dyn Future<Output = Result<models::SplitResponseSchema, Error>> + Send>>;
    fn list_splits_for_file(
        &self,
        file_id: &str,
    ) -> Pin<Box<dyn Future<Output = Result<Vec<models::SplitResponseSchema>, Error>> + Send>>;
    fn vector_search(
        &self,
        split_vector_search_schema: models::SplitVectorSearchSchema,
    ) -> Pin<Box<dyn Future<Output = Result<Vec<models::SplitResponseSchema>, Error>> + Send>>;
}

impl<C: Connect> SplitApi for SplitApiClient<C>
where
    C: Clone + std::marker::Send + Sync,
{
    #[allow(unused_mut)]
    fn get_split(
        &self,
        split_id: &str,
    ) -> Pin<Box<dyn Future<Output = Result<models::SplitResponseSchema, Error>> + Send>> {
        let mut req = __internal_request::Request::new(
            hyper::Method::GET,
            "/api/corpora/split/{split_id}".to_string(),
        );
        req = req.with_path_param("split_id".to_string(), split_id.to_string());

        req.execute(self.configuration.borrow())
    }

    #[allow(unused_mut)]
    fn list_splits_for_file(
        &self,
        file_id: &str,
    ) -> Pin<Box<dyn Future<Output = Result<Vec<models::SplitResponseSchema>, Error>> + Send>> {
        let mut req = __internal_request::Request::new(
            hyper::Method::GET,
            "/api/corpora/split/file/{file_id}".to_string(),
        );
        req = req.with_path_param("file_id".to_string(), file_id.to_string());

        req.execute(self.configuration.borrow())
    }

    #[allow(unused_mut)]
    fn vector_search(
        &self,
        split_vector_search_schema: models::SplitVectorSearchSchema,
    ) -> Pin<Box<dyn Future<Output = Result<Vec<models::SplitResponseSchema>, Error>> + Send>> {
        let mut req = __internal_request::Request::new(
            hyper::Method::POST,
            "/api/corpora/split/search".to_string(),
        );
        req = req.with_body_param(split_vector_search_schema);

        req.execute(self.configuration.borrow())
    }
}
