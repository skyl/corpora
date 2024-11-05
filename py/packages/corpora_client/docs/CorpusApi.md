# corpora_client.CorpusApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**corpora_routers_corpus_create_corpus**](CorpusApi.md#corpora_routers_corpus_create_corpus) | **POST** /api/corpora/corpus | Create Corpus
[**corpora_routers_corpus_delete_corpus**](CorpusApi.md#corpora_routers_corpus_delete_corpus) | **DELETE** /api/corpora/corpus | Delete Corpus
[**corpora_routers_corpus_get_corpus**](CorpusApi.md#corpora_routers_corpus_get_corpus) | **GET** /api/corpora/corpus/{corpus_id} | Get Corpus
[**corpora_routers_corpus_list_corpora**](CorpusApi.md#corpora_routers_corpus_list_corpora) | **GET** /api/corpora/corpus | List Corpora


# **corpora_routers_corpus_create_corpus**
> CorpusResponseSchema corpora_routers_corpus_create_corpus(name, tarball, url=url)

Create Corpus

Create a new Corpus with an uploaded tarball.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.corpus_response_schema import CorpusResponseSchema
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
    api_instance = corpora_client.CorpusApi(api_client)
    name = 'name_example' # str | 
    tarball = None # bytearray | 
    url = 'url_example' # str |  (optional)

    try:
        # Create Corpus
        api_response = api_instance.corpora_routers_corpus_create_corpus(name, tarball, url=url)
        print("The response of CorpusApi->corpora_routers_corpus_create_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->corpora_routers_corpus_create_corpus: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**|  | 
 **tarball** | **bytearray**|  | 
 **url** | **str**|  | [optional] 

### Return type

[**CorpusResponseSchema**](CorpusResponseSchema.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |
**400** | Bad Request |  -  |
**409** | Conflict |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **corpora_routers_corpus_delete_corpus**
> str corpora_routers_corpus_delete_corpus(corpus_name)

Delete Corpus

Delete a Corpus by name.

### Example

* Bearer Authentication (BearerAuth):

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
with corpora_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = corpora_client.CorpusApi(api_client)
    corpus_name = 'corpus_name_example' # str | 

    try:
        # Delete Corpus
        api_response = api_instance.corpora_routers_corpus_delete_corpus(corpus_name)
        print("The response of CorpusApi->corpora_routers_corpus_delete_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->corpora_routers_corpus_delete_corpus: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_name** | **str**|  | 

### Return type

**str**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **corpora_routers_corpus_get_corpus**
> CorpusResponseSchema corpora_routers_corpus_get_corpus(corpus_id)

Get Corpus

Retrieve a Corpus by ID.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.corpus_response_schema import CorpusResponseSchema
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
    api_instance = corpora_client.CorpusApi(api_client)
    corpus_id = 'corpus_id_example' # str | 

    try:
        # Get Corpus
        api_response = api_instance.corpora_routers_corpus_get_corpus(corpus_id)
        print("The response of CorpusApi->corpora_routers_corpus_get_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->corpora_routers_corpus_get_corpus: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_id** | **str**|  | 

### Return type

[**CorpusResponseSchema**](CorpusResponseSchema.md)

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

# **corpora_routers_corpus_list_corpora**
> List[CorpusResponseSchema] corpora_routers_corpus_list_corpora()

List Corpora

List all Corpora.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.corpus_response_schema import CorpusResponseSchema
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
    api_instance = corpora_client.CorpusApi(api_client)

    try:
        # List Corpora
        api_response = api_instance.corpora_routers_corpus_list_corpora()
        print("The response of CorpusApi->corpora_routers_corpus_list_corpora:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->corpora_routers_corpus_list_corpora: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[CorpusResponseSchema]**](CorpusResponseSchema.md)

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

