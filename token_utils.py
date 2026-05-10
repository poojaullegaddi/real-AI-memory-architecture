import tiktoken

encoding = tiktoken.get_encoding(
    "cl100k_base"
)

def count_tokens(messages):

    total_tokens = 0

    for msg in messages:

        tokens = encoding.encode(
            msg["content"]
        )

        total_tokens += len(tokens)

    return total_tokens