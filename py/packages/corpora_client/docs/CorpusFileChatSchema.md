# CorpusFileChatSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**corpus_id** | **str** |  | 
**messages** | [**List[MessageSchema]**](MessageSchema.md) |  | 
**voice** | **str** |  | [optional] [default to '']
**purpose** | **str** |  | [optional] [default to '']
**structure** | **str** |  | [optional] [default to '']
**directions** | **str** |  | [optional] [default to '']
**path** | **str** |  | 

## Example

```python
from corpora_client.models.corpus_file_chat_schema import CorpusFileChatSchema

# TODO update the JSON string below
json = "{}"
# create an instance of CorpusFileChatSchema from a JSON string
corpus_file_chat_schema_instance = CorpusFileChatSchema.from_json(json)
# print the JSON string representation of the object
print(CorpusFileChatSchema.to_json())

# convert the object into a dict
corpus_file_chat_schema_dict = corpus_file_chat_schema_instance.to_dict()
# create an instance of CorpusFileChatSchema from a dict
corpus_file_chat_schema_from_dict = CorpusFileChatSchema.from_dict(corpus_file_chat_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


