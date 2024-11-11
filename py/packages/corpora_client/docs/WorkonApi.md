# corpora_client.WorkonApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_revision**](WorkonApi.md#get_revision) | **POST** /api/corpora/workon/file | File


# **get_revision**
> str get_revision(corpus_file_chat_schema)

File

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.corpus_file_chat_schema import CorpusFileChatSchema
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
with corpora_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = corpora_client.WorkonApi(api_client)
    corpus_file_chat_schema = corpora_client.CorpusFileChatSchema() # CorpusFileChatSchema | 

    try:
        # File
        api_response = api_instance.get_revision(corpus_file_chat_schema)
        print("The response of WorkonApi->get_revision:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WorkonApi->get_revision: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_file_chat_schema** | [**CorpusFileChatSchema**](CorpusFileChatSchema.md)|  | 

### Return type

**str**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

