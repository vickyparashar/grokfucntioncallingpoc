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
    # Ensure that the numbers are integers, then calculate the sum
    result = number1 + number2
    return f"Sum is {result}"


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
    },
    verify=False
)

# Handle the response
if response.status_code == 200:
    response_data = response.json()
    #print("Grok's response:", response_data)

    # Check if there are tool calls in the response
    if 'choices' in response_data and len(response_data['choices']) > 0:
        choice = response_data['choices'][0]
        if 'tool_calls' in choice['message']:
            # Extract the tool call (function call) from the response
            tool_call = choice['message']['tool_calls'][0]
            function_name = tool_call['function']['name']
            arguments = tool_call['function']['arguments']

            # Parse the arguments (assuming it's in JSON string format)
            import json
            args = json.loads(arguments)

            # Simulate Grok calling the function with extracted arguments
            if function_name == 'calculate_sum_of_two_numbers':
                number1 = args['number1']
                number2 = args['number2']
                result = calculate_sum_of_two_numbers(number1, number2)
                print(f"Result of {number1} + {number2} = {result}")
else:
    print(f"Error: {response.status_code} - {response.text}")
