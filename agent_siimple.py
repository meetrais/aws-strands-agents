from strands import Agent
from strands.models.ollama import OllamaModel

# Ollama
ollama_model = OllamaModel(
  host="http://localhost:11434",
  model_id="gemma3"
)
agent = Agent(model=ollama_model)
response = agent("Tell me about agentic AI")
print(response)
