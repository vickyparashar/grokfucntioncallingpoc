import requests

# Define the API key and endpoint
api_key = "xai-1YU6eJGnUgOKmJR6IkBl3zaPy5fNKGjFtN8Dg4zPkdvssXtqWEIlY8zb6LHlS9v7XE9uXVSz3T0h80kQ"
url = "https://api.x.ai/v1/chat/completions"

# Prepare the headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define the function to calculate the sum of two numbers
def calculate_sum_of_two_numbers(number1, number2):
    return number1 + number2

# Updated tools definition with correct schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_sum_of_two_numbers",
            "description": "Calculates the sum of two numbers",
            "parameters": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "integer",
                        "description": "The first number to be added"
                    },
                    "number2": {
                        "type": "integer",
                        "description": "The second number to be added"
                    }
                },
                "required": ["number1", "number2"]
            }
        }
    }
]

# Define the messages for the conversation
messages = [
    {"role": "system", "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."},
    {"role": "user", "content": "Can you sum 4 and 5 for me?"}
]

# Make the request to the AI model with function calling tools
response = requests.post(
    url,
    headers=headers,
    json={
        "model": "grok-beta",
        "messages": messages,
        "tools": tools,
        "tool_choice": "auto",  # Automatically choose a tool (function) if needed
        "max_tokens": 4096
    }
)

# Handle the response
if response.status_code == 200:
    response_data = response.json()
    print("Grok's response:", response_data)

    # # Simulate Grok calling the function if it was part of the response
    # if 'function_call' in response_data:
    #     function_call = response_data['function_call']
    #     if function_call['name'] == 'calculate_sum_of_two_numbers':
    #         params = function_call['parameters']
    #         number1 = params['number1']
    #         number2 = params['number2']
    #         result = calculate_sum_of_two_numbers(number1, number2)
    #         print(f"Result of {number1} + {number2} = {result}")
else:
    print(f"Error: {response.status_code} - {response.text}")
