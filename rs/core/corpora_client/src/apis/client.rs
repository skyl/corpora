use std::sync::Arc;

use hyper;
use hyper_util::client::legacy::connect::Connect;
use super::configuration::Configuration;

pub struct APIClient {
    corpus_api: Box<dyn crate::apis::CorpusApi>,
    file_api: Box<dyn crate::apis::FileApi>,
    plan_api: Box<dyn crate::apis::PlanApi>,
    split_api: Box<dyn crate::apis::SplitApi>,
    workon_api: Box<dyn crate::apis::WorkonApi>,
}

impl APIClient {
    pub fn new<C: Connect>(configuration: Configuration<C>) -> APIClient
        where C: Clone + std::marker::Send + Sync + 'static {
        let rc = Arc::new(configuration);

        APIClient {
            corpus_api: Box::new(crate::apis::CorpusApiClient::new(rc.clone())),
            file_api: Box::new(crate::apis::FileApiClient::new(rc.clone())),
            plan_api: Box::new(crate::apis::PlanApiClient::new(rc.clone())),
            split_api: Box::new(crate::apis::SplitApiClient::new(rc.clone())),
            workon_api: Box::new(crate::apis::WorkonApiClient::new(rc.clone())),
        }
    }

    pub fn corpus_api(&self) -> &dyn crate::apis::CorpusApi{
        self.corpus_api.as_ref()
    }

    pub fn file_api(&self) -> &dyn crate::apis::FileApi{
        self.file_api.as_ref()
    }

    pub fn plan_api(&self) -> &dyn crate::apis::PlanApi{
        self.plan_api.as_ref()
    }

    pub fn split_api(&self) -> &dyn crate::apis::SplitApi{
        self.split_api.as_ref()
    }

    pub fn workon_api(&self) -> &dyn crate::apis::WorkonApi{
        self.workon_api.as_ref()
    }

}
