import json

# JSON data as a string
json_data = '''{
    "id": "704bad67-adf1-48a9-92ea-93d004e9353f",
    "object": "chat.completion",
    "created": 1732788126,
    "model": "grok-beta",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "The sum of 4 and 5 is 9.",
                "tool_calls": [
                    {
                        "id": "0",
                        "function": {
                            "name": "calculate_sum_of_two_numbers",
                            "arguments": "{\"number1\":4,\"number2\":5}"
                        },
                        "type": "function"
                    }
                ],
                "refusal": null
            },
            "finish_reason": "tool_calls"
        }
    ],
    "usage": {
        "prompt_tokens": 202,
        "completion_tokens": 13,
        "total_tokens": 215,
        "prompt_tokens_details": {
            "text_tokens": 202,
            "audio_tokens": 0,
            "image_tokens": 0,
            "cached_tokens": 0
        }
    },
    "system_fingerprint": "fp_6ca29cf396"
}'''

# Parse the JSON
data = json.loads(json_data)

# Accessing specific elements
id = data["id"]
model = data["model"]
message_content = data["choices"][0]["message"]["content"]
tool_function = data["choices"][0]["message"]["tool_calls"][0]["function"]["name"]
arguments = json.loads(data["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])
number1 = arguments["number1"]
number2 = arguments["number2"]

# Print extracted values
print(f"ID: {id}")
print(f"Model: {model}")
print(f"Message Content: {message_content}")
print(f"Function Called: {tool_function}")
print(f"Arguments: number1 = {number1}, number2 = {number2}")
