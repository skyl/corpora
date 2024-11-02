# CorpusResponseSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | 
**url** | **str** |  | [optional] 
**created_at** | **datetime** |  | 
**updated_at** | **datetime** |  | 

## Example

```python
from corpora_client.models.corpus_response_schema import CorpusResponseSchema

# TODO update the JSON string below
json = "{}"
# create an instance of CorpusResponseSchema from a JSON string
corpus_response_schema_instance = CorpusResponseSchema.from_json(json)
# print the JSON string representation of the object
print(CorpusResponseSchema.to_json())

# convert the object into a dict
corpus_response_schema_dict = corpus_response_schema_instance.to_dict()
# create an instance of CorpusResponseSchema from a dict
corpus_response_schema_from_dict = CorpusResponseSchema.from_dict(corpus_response_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


