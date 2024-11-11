# CorpusUpdateFilesSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delete_files** | **List[str]** |  | [optional] 

## Example

```python
from corpora_client.models.corpus_update_files_schema import CorpusUpdateFilesSchema

# TODO update the JSON string below
json = "{}"
# create an instance of CorpusUpdateFilesSchema from a JSON string
corpus_update_files_schema_instance = CorpusUpdateFilesSchema.from_json(json)
# print the JSON string representation of the object
print(CorpusUpdateFilesSchema.to_json())

# convert the object into a dict
corpus_update_files_schema_dict = corpus_update_files_schema_instance.to_dict()
# create an instance of CorpusUpdateFilesSchema from a dict
corpus_update_files_schema_from_dict = CorpusUpdateFilesSchema.from_dict(corpus_update_files_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


