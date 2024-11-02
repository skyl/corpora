# CorpusSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**url** | **str** |  | [optional] 

## Example

```python
from corpora_client.models.corpus_schema import CorpusSchema

# TODO update the JSON string below
json = "{}"
# create an instance of CorpusSchema from a JSON string
corpus_schema_instance = CorpusSchema.from_json(json)
# print the JSON string representation of the object
print(CorpusSchema.to_json())

# convert the object into a dict
corpus_schema_dict = corpus_schema_instance.to_dict()
# create an instance of CorpusSchema from a dict
corpus_schema_from_dict = CorpusSchema.from_dict(corpus_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


