# UpdateCorpusSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_files** | **List[str]** |  | [optional] 

## Example

```python
from corpora_client.models.update_corpus_schema import UpdateCorpusSchema

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateCorpusSchema from a JSON string
update_corpus_schema_instance = UpdateCorpusSchema.from_json(json)
# print the JSON string representation of the object
print(UpdateCorpusSchema.to_json())

# convert the object into a dict
update_corpus_schema_dict = update_corpus_schema_instance.to_dict()
# create an instance of UpdateCorpusSchema from a dict
update_corpus_schema_from_dict = UpdateCorpusSchema.from_dict(update_corpus_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


