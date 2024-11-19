# CorpusChatSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**corpus_id** | **str** |  | 
**messages** | [**List[MessageSchema]**](MessageSchema.md) |  | 
**voice** | **str** |  | [optional] [default to '']
**purpose** | **str** |  | [optional] [default to '']
**structure** | **str** |  | [optional] [default to '']
**directions** | **str** |  | [optional] [default to '']

## Example

```python
from corpora_client.models.corpus_chat_schema import CorpusChatSchema

# TODO update the JSON string below
json = "{}"
# create an instance of CorpusChatSchema from a JSON string
corpus_chat_schema_instance = CorpusChatSchema.from_json(json)
# print the JSON string representation of the object
print(CorpusChatSchema.to_json())

# convert the object into a dict
corpus_chat_schema_dict = corpus_chat_schema_instance.to_dict()
# create an instance of CorpusChatSchema from a dict
corpus_chat_schema_from_dict = CorpusChatSchema.from_dict(corpus_chat_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


