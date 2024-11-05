# SplitVectorSearchSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**corpus_id** | **str** |  | 
**vector** | **List[float]** |  | 
**limit** | **int** |  | [optional] [default to 10]

## Example

```python
from corpora_client.models.split_vector_search_schema import SplitVectorSearchSchema

# TODO update the JSON string below
json = "{}"
# create an instance of SplitVectorSearchSchema from a JSON string
split_vector_search_schema_instance = SplitVectorSearchSchema.from_json(json)
# print the JSON string representation of the object
print(SplitVectorSearchSchema.to_json())

# convert the object into a dict
split_vector_search_schema_dict = split_vector_search_schema_instance.to_dict()
# create an instance of SplitVectorSearchSchema from a dict
split_vector_search_schema_from_dict = SplitVectorSearchSchema.from_dict(split_vector_search_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


