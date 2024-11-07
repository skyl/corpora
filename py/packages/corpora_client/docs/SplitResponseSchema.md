# SplitResponseSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**content** | **str** |  | 
**order** | **int** |  | 
**file_id** | **str** |  | 

## Example

```python
from corpora_client.models.split_response_schema import SplitResponseSchema

# TODO update the JSON string below
json = "{}"
# create an instance of SplitResponseSchema from a JSON string
split_response_schema_instance = SplitResponseSchema.from_json(json)
# print the JSON string representation of the object
print(SplitResponseSchema.to_json())

# convert the object into a dict
split_response_schema_dict = split_response_schema_instance.to_dict()
# create an instance of SplitResponseSchema from a dict
split_response_schema_from_dict = SplitResponseSchema.from_dict(split_response_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


