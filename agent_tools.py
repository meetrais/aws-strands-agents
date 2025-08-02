from strands import Agent
from strands.models.bedrock import BedrockModel
from custom_tool import invoke_bedrock
from strands_tools import calculator, current_time
from dotenv import load_dotenv
import os

load_dotenv()

# Try to create a proper Agent with multiple approaches
def create_working_agent():
    """Try different agent configurations to find one that works."""
    
    # First, try with a standard Bedrock model that might work
    try:
        print("🔧 Attempting Agent with standard Claude 3.5 Sonnet...")
        bedrock_model = BedrockModel(
            model_id="anthropic.claude-3-5-sonnet-20241022-v2:0",
            region="us-east-1"
        )
        agent = Agent(model=bedrock_model, tools=[calculator, current_time, invoke_bedrock])
        
        # Test with a simple query first
        test_response = agent("What is 2+2?")
        print("✅ Standard Bedrock Agent working!")
        return agent
        
    except Exception as e:
        print(f"❌ Standard Bedrock failed: {e}")
    
    # If standard Bedrock fails, try with our custom tool as the main model interface
    try:
        print("🔧 Creating hybrid approach with custom Bedrock tool...")
        # Use a minimal working model for orchestration, custom tool for Bedrock
        from strands.models.openai import OpenAIModel
        
        # Try with OpenAI as orchestrator (if available)
        openai_model = OpenAIModel(model_id="gpt-3.5-turbo")
        agent = Agent(model=openai_model, tools=[calculator, current_time, invoke_bedrock])
        print("✅ Hybrid Agent with OpenAI orchestrator created!")
        return agent
        
    except Exception as e:
        print(f"❌ OpenAI hybrid failed: {e}")
        
    return None

def run_agentic_workflow():
    """Run the agentic workflow with proper tool calling."""
    
    agent = create_working_agent()
    
    if agent:
        print("\n🤖 Running Agentic Workflow...")
        print("=" * 50)
        
        # Let the agent decide which tools to use for the complex query
        query = """I need you to:
        1. Find the square root of 1764 using the most appropriate tool
        2. Tell me the current time
        3. Verify your square root calculation using the calculator tool
        
        Please use the available tools to complete these tasks and explain your reasoning."""
        
        try:
            response = agent(query)
            print("🎯 Agent Response:")
            print(response)
            
        except Exception as e:
            print(f"❌ Agent execution failed: {e}")
            print("\n🔄 Falling back to tool orchestration...")
            fallback_execution()
    else:
        print("\n⚠️ Could not create working agent. Using tool orchestration...")
        fallback_execution()

def fallback_execution():
    """Fallback that simulates agentic behavior with direct tool calls."""
    print("\n🔧 Orchestrating tools manually with reasoning...")
    
    print("\n💭 Reasoning: I need to find the square root of 1764.")
    print("🔧 Selecting tool: invoke_bedrock (for advanced mathematical reasoning)")
    bedrock_response = invoke_bedrock("What is the square root of 1764? Show your work.")
    print("📊 Bedrock Response:")
    print(bedrock_response)
    
    print("\n💭 Reasoning: Let me verify this with the calculator tool.")
    print("🔧 Selecting tool: calculator (for verification)")
    from strands_tools.calculator import calculator
    calc_result = calculator("sqrt(1764)")
    print("📊 Calculator verification:")
    print(calc_result)
    
    print("\n💭 Reasoning: Now I need to get the current time.")
    print("🔧 Selecting tool: current_time")
    from strands_tools.current_time import current_time
    time_result = current_time()
    print("📊 Current time:")
    print(f"The current time is: {time_result}")
    
    print("\n✅ Task completed using intelligent tool selection!")

if __name__ == "__main__":
    run_agentic_workflow()
