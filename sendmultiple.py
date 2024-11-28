import requests
import json

# Define the function to calculate the sum of two numbers
def calculate_sum_of_two_numbers(number1, number2):
    result = number1 + number2
    return f"Sum is {result}"

# Define any additional functions as needed (for example)
# def another_function(...): ...

# Function to handle conversation and function calls
def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": "You are a function calling LLM that uses the data extracted from the functions to answer questions around various topics."
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    
    # API Key and endpoint
    api_key = "xai-1YU6eJGnUgOKmJR6IkBl3zaPy5fNKGjFtN8Dg4zPkdvssXtqWEIlY8zb6LHlS9v7XE9uXVSz3T0h80kQ"
    url = "https://api.x.ai/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Tools definition (update with all available functions)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_sum_of_two_numbers",
                "description": "Calculates the sum of two numbers",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "number1": {"type": "integer", "description": "First number"},
                        "number2": {"type": "integer", "description": "Second number"}
                    },
                    "required": ["number1", "number2"]
                }
            }
        }
    ]

    # Available functions to call dynamically
    available_functions = {
        "calculate_sum_of_two_numbers": calculate_sum_of_two_numbers,
        # Add more functions here as needed
    }

    while True:
        # Send request to the model
        response = requests.post(
            url,
            headers=headers,
            json={
                "model": "grok-beta",
                "messages": messages,
                "tools": tools,
                "tool_choice": "auto",
                "max_tokens": 4096
            },
            verify=False
        )

        if response.status_code == 200:
            response_data = response.json()
            response_message = response_data['choices'][0]['message']
            tool_calls = response_message.get('tool_calls', [])

            # If there are function calls, process them
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call['function']['name']
                    function_args = json.loads(tool_call['function']['arguments'])
                    
                    # Ensure the function is available
                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        function_response = function_to_call(**function_args)

                        # Append the function's response to messages
                        messages.append({
                            "tool_call_id": tool_call['id'],
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        })
                    else:
                        print(f"Function {function_name} not available.")
                
                # Continue the loop for another request with updated messages
                continue
            else:
                # No further function calls, return the final response
                final_response = response_data['choices'][0]['message']['content']
                return final_response
        else:
            print(f"Error: {response.status_code} - {response.text}")
            break

# Example of using the function
user_prompt = "Can you sum 4 and 5 for me?"
final_response = run_conversation(user_prompt)
print(final_response)
