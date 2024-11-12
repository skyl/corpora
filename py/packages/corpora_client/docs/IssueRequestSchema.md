# IssueRequestSchema


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
from corpora_client.models.issue_request_schema import IssueRequestSchema

# TODO update the JSON string below
json = "{}"
# create an instance of IssueRequestSchema from a JSON string
issue_request_schema_instance = IssueRequestSchema.from_json(json)
# print the JSON string representation of the object
print(IssueRequestSchema.to_json())

# convert the object into a dict
issue_request_schema_dict = issue_request_schema_instance.to_dict()
# create an instance of IssueRequestSchema from a dict
issue_request_schema_from_dict = IssueRequestSchema.from_dict(issue_request_schema_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


