# corpora_client.CorpusApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_corpus**](CorpusApi.md#create_corpus) | **POST** /api/corpora/corpus | Create Corpus
[**delete_corpus**](CorpusApi.md#delete_corpus) | **DELETE** /api/corpora/corpus | Delete Corpus
[**get_corpus**](CorpusApi.md#get_corpus) | **GET** /api/corpora/corpus/{corpus_id} | Get Corpus
[**get_file_hashes**](CorpusApi.md#get_file_hashes) | **GET** /api/corpora/corpus/{corpus_id}/files | Get File Hashes
[**list_corpora**](CorpusApi.md#list_corpora) | **GET** /api/corpora/corpus | List Corpora
[**update_files**](CorpusApi.md#update_files) | **POST** /api/corpora/corpus/{corpus_id}/files | Update Files


# **create_corpus**
> CorpusResponseSchema create_corpus(name, tarball, url=url)

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
        api_response = api_instance.create_corpus(name, tarball, url=url)
        print("The response of CorpusApi->create_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->create_corpus: %s\n" % e)
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

# **delete_corpus**
> str delete_corpus(corpus_name)

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
        api_response = api_instance.delete_corpus(corpus_name)
        print("The response of CorpusApi->delete_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->delete_corpus: %s\n" % e)
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

# **get_corpus**
> CorpusResponseSchema get_corpus(corpus_id)

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
        api_response = api_instance.get_corpus(corpus_id)
        print("The response of CorpusApi->get_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->get_corpus: %s\n" % e)
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

# **get_file_hashes**
> Dict[str, str] get_file_hashes(corpus_id)

Get File Hashes

Retrieve a map of file paths to their hashes for a Corpus.

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
    corpus_id = 'corpus_id_example' # str | 

    try:
        # Get File Hashes
        api_response = api_instance.get_file_hashes(corpus_id)
        print("The response of CorpusApi->get_file_hashes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->get_file_hashes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_id** | **str**|  | 

### Return type

**Dict[str, str]**

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

# **list_corpora**
> List[CorpusResponseSchema] list_corpora()

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
        api_response = api_instance.list_corpora()
        print("The response of CorpusApi->list_corpora:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->list_corpora: %s\n" % e)
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

# **update_files**
> str update_files(corpus_id, tarball, delete_files=delete_files)

Update Files

Update a Corpus with an uploaded tarball for additions/updates and a list of files to delete

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
    corpus_id = 'corpus_id_example' # str | 
    tarball = None # bytearray | 
    delete_files = ['delete_files_example'] # List[str] |  (optional)

    try:
        # Update Files
        api_response = api_instance.update_files(corpus_id, tarball, delete_files=delete_files)
        print("The response of CorpusApi->update_files:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorpusApi->update_files: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_id** | **str**|  | 
 **tarball** | **bytearray**|  | 
 **delete_files** | [**List[str]**](str.md)|  | [optional] 

### Return type

**str**

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: multipart/form-data
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |
**404** | Not Found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

