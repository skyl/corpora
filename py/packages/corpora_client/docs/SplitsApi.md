# corpora_client.SplitsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**corpora_routers_split_get_split**](SplitsApi.md#corpora_routers_split_get_split) | **GET** /api/corpora/split/{split_id} | Get Split
[**corpora_routers_split_list_splits_for_file**](SplitsApi.md#corpora_routers_split_list_splits_for_file) | **GET** /api/corpora/split/file/{file_id} | List Splits For File
[**corpora_routers_split_vector_search_splits**](SplitsApi.md#corpora_routers_split_vector_search_splits) | **POST** /api/corpora/split/search | Vector Search Splits


# **corpora_routers_split_get_split**
> SplitResponseSchema corpora_routers_split_get_split(split_id)

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
    api_instance = corpora_client.SplitsApi(api_client)
    split_id = 'split_id_example' # str | 

    try:
        # Get Split
        api_response = api_instance.corpora_routers_split_get_split(split_id)
        print("The response of SplitsApi->corpora_routers_split_get_split:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->corpora_routers_split_get_split: %s\n" % e)
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

# **corpora_routers_split_list_splits_for_file**
> List[SplitResponseSchema] corpora_routers_split_list_splits_for_file(file_id)

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
    api_instance = corpora_client.SplitsApi(api_client)
    file_id = 'file_id_example' # str | 

    try:
        # List Splits For File
        api_response = api_instance.corpora_routers_split_list_splits_for_file(file_id)
        print("The response of SplitsApi->corpora_routers_split_list_splits_for_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->corpora_routers_split_list_splits_for_file: %s\n" % e)
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

# **corpora_routers_split_vector_search_splits**
> List[SplitResponseSchema] corpora_routers_split_vector_search_splits(split_vector_search_schema)

Vector Search Splits

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
    api_instance = corpora_client.SplitsApi(api_client)
    split_vector_search_schema = corpora_client.SplitVectorSearchSchema() # SplitVectorSearchSchema | 

    try:
        # Vector Search Splits
        api_response = api_instance.corpora_routers_split_vector_search_splits(split_vector_search_schema)
        print("The response of SplitsApi->corpora_routers_split_vector_search_splits:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling SplitsApi->corpora_routers_split_vector_search_splits: %s\n" % e)
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

