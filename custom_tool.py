import boto3
import json
import os
from dotenv import load_dotenv
from strands import tool

load_dotenv()

@tool
def invoke_bedrock(prompt: str) -> str:
    """
    Invokes the Bedrock model with the given prompt.
    """
    try:
        # Create a Bedrock client
        bedrock = boto3.client(service_name='bedrock-runtime', region_name='us-east-2')

        # Set the model ARN
        model_arn = os.getenv("MODEL_ARN")

        # Create the request body
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}],
                }
            ],
        })

        # Invoke the model
        response = bedrock.invoke_model(body=body, modelId=model_arn)

        # Process and print the response
        response_body = json.loads(response.get('body').read())
        return response_body['content'][0]['text']

    except Exception as e:
        return f"An error occurred: {e}"
