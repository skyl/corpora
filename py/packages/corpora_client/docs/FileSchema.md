# FileSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path** | **str** |  | 
**content** | **str** |  | 
**corpus_id** | **str** |  | 

## Example

```python
from corpora_client.models.file_schema import FileSchema

# TODO update the JSON string below
json = "{}"
# create an instance of FileSchema from a JSON string
file_schema_instance = FileSchema.from_json(json)
# print the JSON string representation of the object
print(FileSchema.to_json())

# convert the object into a dict
file_schema_dict = file_schema_instance.to_dict()
# create an instance of FileSchema from a dict
file_schema_from_dict = FileSchema.from_dict(file_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


