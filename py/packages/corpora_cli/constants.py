from rich.markdown import Markdown

NO_AUTHENTICATION_MESSAGE = Markdown(
    """
Currently we support **Client Credential** authentication.

Check the **server** in your `.corpora.yaml` file and make sure the `base_url` is correct.

Then, in your CLI environment, set the following environment variables:

- `CORPORA_CLIENT_ID`
- `CORPORA_CLIENT_SECRET`

```bash
export CORPORA_CLIENT_ID="{your_client_id}"
export CORPORA_CLIENT_SECRET="{your_client_secret}"
```
"""
)
