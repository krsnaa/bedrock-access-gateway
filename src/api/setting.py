import os

DEFAULT_API_KEYS = "kiku-bedrock-key"

API_ROUTE_PREFIX = "/api/v1"
AZURE_API_ROUTE_PREFIX = "/openai/deployments/kiku-deployment"

TITLE = "Amazon Bedrock Proxy APIs"
SUMMARY = "OpenAI-Compatible RESTful APIs for Amazon Bedrock"
VERSION = "0.1.0"
DESCRIPTION = """
Use OpenAI-Compatible RESTful APIs for Amazon Bedrock models.

List of Amazon Bedrock models currently supported:
- Anthropic Claude 2 / 3 /3.5 (Haiku/Sonnet/Opus)
- Meta Llama 2 / 3
- Mistral / Mixtral
- Cohere Command R / R+
- Cohere Embedding
"""

DEBUG = os.environ.get("DEBUG", "false").lower() != "false"
AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")
DEFAULT_MODEL = os.environ.get(
    "DEFAULT_MODEL", "anthropic.claude-3-5-sonnet-20240620-v1:0"
)
DEFAULT_EMBEDDING_MODEL = os.environ.get(
    "DEFAULT_EMBEDDING_MODEL", "cohere.embed-multilingual-v3"
)
