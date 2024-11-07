# corpora_client.SplitApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_split**](SplitApi.md#get_split) | **GET** /api/corpora/split/{split_id} | Get Split
[**list_splits_for_file**](SplitApi.md#list_splits_for_file) | **GET** /api/corpora/split/file/{file_id} | List Splits For File
[**vector_search**](SplitApi.md#vector_search) | **POST** /api/corpora/split/search | Vector Search


# **get_split**
> SplitResponseSchema get_split(split_id)

Get Split

Retrieve a Split by ID.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.split_response_schema import SplitResponseSchema
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
    api_instance = corpora_client.SplitApi(api_client)
    split_id = 'split_id_example' # str | 

    try:
        # Get Split
        api_response = api_instance.get_split(split_id)
        print("The response of SplitApi->get_split:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitApi->get_split: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **split_id** | **str**|  | 

### Return type

[**SplitResponseSchema**](SplitResponseSchema.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **list_splits_for_file**
> List[SplitResponseSchema] list_splits_for_file(file_id)

List Splits For File

List all Splits for a specific CorpusTextFile.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.split_response_schema import SplitResponseSchema
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
    api_instance = corpora_client.SplitApi(api_client)
    file_id = 'file_id_example' # str | 

    try:
        # List Splits For File
        api_response = api_instance.list_splits_for_file(file_id)
        print("The response of SplitApi->list_splits_for_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitApi->list_splits_for_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**|  | 

### Return type

[**List[SplitResponseSchema]**](SplitResponseSchema.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vector_search**
> List[SplitResponseSchema] vector_search(split_vector_search_schema)

Vector Search

Perform a vector similarity search for splits using a provided query vector.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.split_response_schema import SplitResponseSchema
from corpora_client.models.split_vector_search_schema import SplitVectorSearchSchema
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
    api_instance = corpora_client.SplitApi(api_client)
    split_vector_search_schema = corpora_client.SplitVectorSearchSchema() # SplitVectorSearchSchema | 

    try:
        # Vector Search
        api_response = api_instance.vector_search(split_vector_search_schema)
        print("The response of SplitApi->vector_search:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitApi->vector_search: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **split_vector_search_schema** | [**SplitVectorSearchSchema**](SplitVectorSearchSchema.md)|  | 

### Return type

[**List[SplitResponseSchema]**](SplitResponseSchema.md)

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

