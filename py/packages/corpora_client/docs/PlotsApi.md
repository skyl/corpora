# corpora_client.PlotsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_matplotlib_plot**](PlotsApi.md#get_matplotlib_plot) | **POST** /api/corpora/plots/matplotlib | Get Matplotlib Plot


# **get_matplotlib_plot**
> PlotResponseSchema get_matplotlib_plot(corpus_chat_schema)

Get Matplotlib Plot

### Example

* Bearer Authentication (BearerAuth):

```python
import corpora_client
from corpora_client.models.corpus_chat_schema import CorpusChatSchema
from corpora_client.models.plot_response_schema import PlotResponseSchema
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
    api_instance = corpora_client.PlotsApi(api_client)
    corpus_chat_schema = corpora_client.CorpusChatSchema() # CorpusChatSchema | 

    try:
        # Get Matplotlib Plot
        api_response = api_instance.get_matplotlib_plot(corpus_chat_schema)
        print("The response of PlotsApi->get_matplotlib_plot:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling PlotsApi->get_matplotlib_plot: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **corpus_chat_schema** | [**CorpusChatSchema**](CorpusChatSchema.md)|  | 

### Return type

[**PlotResponseSchema**](PlotResponseSchema.md)

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

