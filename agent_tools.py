from custom_tool import invoke_bedrock
from strands_tools.current_time import current_time

# Get the answer from Bedrock
bedrock_response = invoke_bedrock("What is the square root of 1764?")
print(bedrock_response)

# Get the current time
time_response = current_time()
print(f"The current time is: {time_response}")
