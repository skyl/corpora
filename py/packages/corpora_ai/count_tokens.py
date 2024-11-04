import tiktoken


def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Counts the number of tokens in a given text string for a specific model.

    Args:
        text (str): The text to count tokens for.
        model (str): The model to base the tokenization on. Default is "gpt-3.5-turbo".

    Returns:
        int: The number of tokens in the text.
    """
    # Load the tokenizer for the specified model
    encoding = tiktoken.encoding_for_model(model)

    # Encode the text and count the tokens
    tokens = encoding.encode(text)
    return len(tokens)
