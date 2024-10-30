# corpora_client.CorporaApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**corpora_api_create_corpus**](CorporaApi.md#corpora_api_create_corpus) | **POST** /api/corpora/corpus | Create Corpus
[**corpora_api_create_file**](CorporaApi.md#corpora_api_create_file) | **POST** /api/corpora/file | Create File
[**corpora_api_get_corpus**](CorporaApi.md#corpora_api_get_corpus) | **GET** /api/corpora/corpus/{corpus_id} | Get Corpus
[**corpora_api_get_file**](CorporaApi.md#corpora_api_get_file) | **GET** /api/corpora/file/{file_id} | Get File
[**corpora_api_list_corpora**](CorporaApi.md#corpora_api_list_corpora) | **GET** /api/corpora/corpus | List Corpora


# **corpora_api_create_corpus**
> CorpusResponseSchema corpora_api_create_corpus(corpus_schema)

Create Corpus

Create a new Corpus.

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.corpus_response_schema import CorpusResponseSchema
from corpora_client.models.corpus_schema import CorpusSchema
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
    api_instance = corpora_client.CorporaApi(api_client)
    corpus_schema = corpora_client.CorpusSchema() # CorpusSchema | 

    try:
        # Create Corpus
        api_response = api_instance.corpora_api_create_corpus(corpus_schema)
        print("The response of CorporaApi->corpora_api_create_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorporaApi->corpora_api_create_corpus: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_schema** | [**CorpusSchema**](CorpusSchema.md)|  | 

### Return type

[**CorpusResponseSchema**](CorpusResponseSchema.md)

### Authorization

[BearerAuth](../README.md#BearerAuth)

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Created |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **corpora_api_create_file**
> FileResponseSchema corpora_api_create_file(file_schema)

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
    api_instance = corpora_client.CorporaApi(api_client)
    file_schema = corpora_client.FileSchema() # FileSchema | 

    try:
        # Create File
        api_response = api_instance.corpora_api_create_file(file_schema)
        print("The response of CorporaApi->corpora_api_create_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorporaApi->corpora_api_create_file: %s\n" % e)
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

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **corpora_api_get_corpus**
> CorpusResponseSchema corpora_api_get_corpus(corpus_id)

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
    api_instance = corpora_client.CorporaApi(api_client)
    corpus_id = 'corpus_id_example' # str | 

    try:
        # Get Corpus
        api_response = api_instance.corpora_api_get_corpus(corpus_id)
        print("The response of CorporaApi->corpora_api_get_corpus:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorporaApi->corpora_api_get_corpus: %s\n" % e)
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

# **corpora_api_get_file**
> FileResponseSchema corpora_api_get_file(file_id)

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
    api_instance = corpora_client.CorporaApi(api_client)
    file_id = 'file_id_example' # str | 

    try:
        # Get File
        api_response = api_instance.corpora_api_get_file(file_id)
        print("The response of CorporaApi->corpora_api_get_file:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorporaApi->corpora_api_get_file: %s\n" % e)
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

# **corpora_api_list_corpora**
> List[CorpusResponseSchema] corpora_api_list_corpora()

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
    api_instance = corpora_client.CorporaApi(api_client)

    try:
        # List Corpora
        api_response = api_instance.corpora_api_list_corpora()
        print("The response of CorporaApi->corpora_api_list_corpora:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CorporaApi->corpora_api_list_corpora: %s\n" % e)
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

