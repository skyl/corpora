# corpora_client.FileApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_file**](FileApi.md#create_file) | **POST** /api/corpora/file | Create File
[**get_file**](FileApi.md#get_file) | **GET** /api/corpora/file/{file_id} | Get File
[**get_file_by_path**](FileApi.md#get_file_by_path) | **GET** /api/corpora/file/corpus/{corpus_id} | Get File By Path


# **create_file**
> FileResponseSchema create_file(file_schema)

Create File

Create a new File within a Corpus.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.file_response_schema import FileResponseSchema
from corpora_client.models.file_schema import FileSchema
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
    api_instance = corpora_client.FileApi(api_client)
    file_schema = corpora_client.FileSchema() # FileSchema | 

    try:
        # Create File
        api_response = api_instance.create_file(file_schema)
        print("The response of FileApi->create_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileApi->create_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_schema** | [**FileSchema**](FileSchema.md)|  | 

### Return type

[**FileResponseSchema**](FileResponseSchema.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**409** | Conflict |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_file**
> FileResponseSchema get_file(file_id)

Get File

Retrieve a File by ID.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.file_response_schema import FileResponseSchema
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
    api_instance = corpora_client.FileApi(api_client)
    file_id = 'file_id_example' # str | 

    try:
        # Get File
        api_response = api_instance.get_file(file_id)
        print("The response of FileApi->get_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileApi->get_file: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **file_id** | **str**|  | 

### Return type

[**FileResponseSchema**](FileResponseSchema.md)

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

# **get_file_by_path**
> FileResponseSchema get_file_by_path(corpus_id, path)

Get File By Path

Retrieve a File by path within a Corpus.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.file_response_schema import FileResponseSchema
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
    api_instance = corpora_client.FileApi(api_client)
    corpus_id = 'corpus_id_example' # str | 
    path = 'path_example' # str | Path to the file

    try:
        # Get File By Path
        api_response = api_instance.get_file_by_path(corpus_id, path)
        print("The response of FileApi->get_file_by_path:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FileApi->get_file_by_path: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_id** | **str**|  | 
 **path** | **str**| Path to the file | 

### Return type

[**FileResponseSchema**](FileResponseSchema.md)

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

