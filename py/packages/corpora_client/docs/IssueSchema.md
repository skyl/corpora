# IssueSchema


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** |  | 
**body** | **str** |  | 

## Example

```python
from corpora_client.models.issue_schema import IssueSchema

# TODO update the JSON string below
json = "{}"
# create an instance of IssueSchema from a JSON string
issue_schema_instance = IssueSchema.from_json(json)
# print the JSON string representation of the object
print(IssueSchema.to_json())

# convert the object into a dict
issue_schema_dict = issue_schema_instance.to_dict()
# create an instance of IssueSchema from a dict
issue_schema_from_dict = IssueSchema.from_dict(issue_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


