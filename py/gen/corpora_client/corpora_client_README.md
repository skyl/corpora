# corpora-client
No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

The `corpora_client` package is automatically generated by the [OpenAPI Generator](https://openapi-generator.tech) project:

- API version: 1.0.0
- Package version: 1.0.0
- Generator version: 7.9.0
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Requirements.

Python 3.7+

## Installation & Usage

This python library package is generated without supporting files like setup.py or requirements files

To be able to use it, you will need these dependencies in your own package that uses this library:

* urllib3 >= 1.25.3, < 3.0.0
* python-dateutil >= 2.8.2
* aiohttp >= 3.8.4
* aiohttp-retry >= 2.8.3
* pydantic >= 2
* typing-extensions >= 4.7.1

## Getting Started

In your own code, to use this library to connect and interact with corpora-client,
you can run the following:

```python

import corpora_client
from corpora_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = corpora_client.Configuration(
    host = "http://localhost"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure Bearer authorization: BearerAuth
configuration = corpora_client.Configuration(
    access_token = os.environ["BEARER_TOKEN"]
)


# Enter a context with an instance of the API client
async with corpora_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = corpora_client.CorporaApi(api_client)
    corpus_schema = corpora_client.CorpusSchema() # CorpusSchema | 

    try:
        # Create Corpus
        api_response = await api_instance.corpora_api_create_corpus(corpus_schema)
        print("The response of CorporaApi->corpora_api_create_corpus:\n")
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling CorporaApi->corpora_api_create_corpus: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *http://localhost*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*CorporaApi* | [**corpora_api_create_corpus**](corpora_client/docs/CorporaApi.md#corpora_api_create_corpus) | **POST** /api/corpora/corpus | Create Corpus
*CorporaApi* | [**corpora_api_create_file**](corpora_client/docs/CorporaApi.md#corpora_api_create_file) | **POST** /api/corpora/file | Create File
*CorporaApi* | [**corpora_api_get_corpus**](corpora_client/docs/CorporaApi.md#corpora_api_get_corpus) | **GET** /api/corpora/corpus/{corpus_id} | Get Corpus
*CorporaApi* | [**corpora_api_get_file**](corpora_client/docs/CorporaApi.md#corpora_api_get_file) | **GET** /api/corpora/file/{file_id} | Get File


## Documentation For Models

 - [CorpusResponseSchema](corpora_client/docs/CorpusResponseSchema.md)
 - [CorpusSchema](corpora_client/docs/CorpusSchema.md)
 - [FileResponseSchema](corpora_client/docs/FileResponseSchema.md)
 - [FileSchema](corpora_client/docs/FileSchema.md)


<a id="documentation-for-authorization"></a>
## Documentation For Authorization


Authentication schemes defined for the API:
<a id="BearerAuth"></a>
### BearerAuth

- **Type**: Bearer authentication


## Author



