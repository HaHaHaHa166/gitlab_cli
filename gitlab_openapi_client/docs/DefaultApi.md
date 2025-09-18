# openapi_client.DefaultApi

All URIs are relative to *https://gitlab.boon.com.au/api/v4*

Method | HTTP request | Description
------------- | ------------- | -------------
[**projects_get**](DefaultApi.md#projects_get) | **GET** /projects | List projects (minimal)


# **projects_get**
> List[Project] projects_get(per_page=per_page, page=page)

List projects (minimal)

### Example

* Api Key Authentication (ApiKeyAuth):

```python
import openapi_client
from openapi_client.models.project import Project
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to https://gitlab.boon.com.au/api/v4
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "https://gitlab.boon.com.au/api/v4"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: ApiKeyAuth
configuration.api_key['ApiKeyAuth'] = os.environ["API_KEY"]

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['ApiKeyAuth'] = 'Bearer'

# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.DefaultApi(api_client)
    per_page = 20 # int |  (optional) (default to 20)
    page = 1 # int |  (optional) (default to 1)

    try:
        # List projects (minimal)
        api_response = api_instance.projects_get(per_page=per_page, page=page)
        print("The response of DefaultApi->projects_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->projects_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **per_page** | **int**|  | [optional] [default to 20]
 **page** | **int**|  | [optional] [default to 1]

### Return type

[**List[Project]**](Project.md)

### Authorization

[ApiKeyAuth](../README.md#ApiKeyAuth)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | A list of projects |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

