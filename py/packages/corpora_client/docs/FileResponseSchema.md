# FileResponseSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**path** | **str** |  | 
**content** | **str** |  | 
**checksum** | **str** |  | 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 
**corpus** | [**CorpusResponseSchema**](CorpusResponseSchema.md) |  | 

## Example

```python
from corpora_client.models.file_response_schema import FileResponseSchema

# TODO update the JSON string below
json = "{}"
# create an instance of FileResponseSchema from a JSON string
file_response_schema_instance = FileResponseSchema.from_json(json)
# print the JSON string representation of the object
print(FileResponseSchema.to_json())

# convert the object into a dict
file_response_schema_dict = file_response_schema_instance.to_dict()
# create an instance of FileResponseSchema from a dict
file_response_schema_from_dict = FileResponseSchema.from_dict(file_response_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


