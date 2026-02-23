"""Meme Generator Agent - Browser Use Automation."""

# Disable Browser Use telemetry immediately to prevent PostHog errors
import os
os.environ["ANONYMIZED_TELEMETRY"] = "false"
os.environ["BROWSER_USE_TELEMETRY"] = "false"

import argparse
import asyncio
import json
import re
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from bindu.penguin.bindufy import bindufy
from browser_use import Agent as BrowserAgent
from browser_use.llm.openai.chat import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

# Global instances
llm: ChatOpenAI | None = None
_initialized = False
_init_lock = asyncio.Lock()


@dataclass
class AgentResponse:
    """Mock response class to match Agno's RunResponse structure."""
    content: str
    run_id: Optional[str] = None
    status: str = "COMPLETED"


def load_config() -> dict:
    """Load agent configuration from project root."""
    possible_paths = [
        Path(__file__).parent.parent / "agent_config.json",
        Path(__file__).parent / "agent_config.json",
        Path.cwd() / "agent_config.json",
    ]

    for config_path in possible_paths:
        if config_path.exists():
            try:
                with open(config_path) as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error reading {config_path}: {type(e).__name__}")
                continue

    return {
        "name": "meme-generator-agent",
        "description": "AI Agent that generates memes using browser automation",
        "version": "1.0.0",
        "deployment": {
            "url": "http://127.0.0.1:3773",
            "expose": True,
            "protocol_version": "1.0.0",
        }
    }


async def initialize_agent() -> None:
    """Initialize the LLM for the browser agent."""
    global llm

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = None

    if not api_key:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if api_key:
             base_url = "https://openrouter.ai/api/v1" 

    if not api_key:
        # Fallback for local testing if env vars aren't set
        print("⚠️ No API Key found in env, checking args...")

    model_name = os.getenv("MODEL_NAME", "gpt-4o")

    if api_key:
        llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,
            temperature=0.0
        )
        print(f"✅ Agent initialized with model: {model_name}")
    else:
        print("❌ Failed to initialize LLM: Missing API Key")


async def generate_meme(query: str) -> str:
    """Run the browser agent to generate a meme."""
    global llm
    if not llm:
        return "Error: Agent not initialized correctly. Please check API keys."

    print(f"🎨 Generating meme for query: {query}")

    task_description = (
        "You are a meme generator expert. You are given a query and you need to generate a meme for it.\n"
        "1. Go to https://imgflip.com/memetemplates \n"
        "2. Click on the Search bar in the middle and search for ONLY ONE MAIN ACTION VERB (like 'bully', 'laugh', 'cry') in this query: '{0}'\n"
        "3. Choose any meme template that metaphorically fits the meme topic: '{0}'\n"
        "   by clicking on the 'Add Caption' button below it\n"
        "4. Write a Top Text (setup/context) and Bottom Text (punchline/outcome) related to '{0}'.\n" 
        "5. Check the preview making sure it is funny and a meaningful meme. Adjust text directly if needed. \n"
        "6. Look at the meme and text on it, if it doesnt make sense, PLEASE retry by filling the text boxes with different text. \n"
        "7. Click on the Generate meme button to generate the meme\n"
        "8. Copy the image link and give it as the output. The link usually looks like 'https://imgflip.com/i/.....'\n"
    ).format(query)

    agent = BrowserAgent(
        task=task_description,
        llm=llm,
        max_actions_per_step=15,  # Increased steps for safety
        max_failures=3,
        use_vision=True 
    )

    try:
        history = await agent.run()
        final_result = history.final_result()
        
        print(f"📄 Raw Agent Result: {final_result}")

        if not final_result:
            return "The agent completed the task but returned no result."

        # Extract meme URL
        # Pattern matches https://imgflip.com/i/ followed by alphanumeric chars
        url_match = re.search(r'https://imgflip\.com/i/([a-zA-Z0-9]+)', final_result)
        
        if url_match:
            meme_id = url_match.group(1)
            # Markdown image syntax for UI rendering
            image_url = f"https://i.imgflip.com/{meme_id}.jpg"
            return f"### Here is your meme:\n\n![Generated Meme]({image_url})\n\n[View on ImgFlip](https://imgflip.com/i/{meme_id})"
        
        # Fallback: Check if there's any HTTP link
        http_match = re.search(r'(https?://[^\s]+)', final_result)
        if http_match:
             link = http_match.group(1)
             return f"I generated a meme, but couldn't confirm the image format. Link: {link}"
             
        return f"I finished the task, but here is what I found: {final_result}"
        
    except Exception as e:
        traceback.print_exc()
        return f"Error generating meme: {str(e)}"


async def handler(messages: list[dict[str, str]]) -> AgentResponse:
    """Handle incoming agent messages."""
    global _initialized

    # Lazy initialization
    async with _init_lock:
        if not _initialized:
            print("🔧 Initializing Meme Generator Agent...")
            await initialize_agent()
            _initialized = True

    # Extract the user's latest query
    user_query = next((m["content"] for m in reversed(messages) if m["role"] == "user"), None)

    if not user_query:
        return AgentResponse(content="Please provide a description for the meme you want to generate.")

    # Run the meme generation logic
    result_text = await generate_meme(user_query)
    
    # Return response object with content attribute
    return AgentResponse(content=result_text)


def main():
    """Run the main entry point for the Agent."""
    parser = argparse.ArgumentParser(description="Meme Generator Agent")
    parser.add_argument("--openai-api-key", type=str, help="OpenAI API key")
    parser.add_argument("--model", type=str, default="gpt-4o", help="Model name")
    
    args = parser.parse_args()

    if args.openai_api_key:
        os.environ["OPENAI_API_KEY"] = args.openai_api_key
    if args.model:
        os.environ["MODEL_NAME"] = args.model

    print("🥸 Meme Generator Agent - Browser Use")
    
    config = load_config()

    try:
        print("🚀 Starting Bindu Agent server...")
        bindufy(config, handler)
    except KeyboardInterrupt:
        print("\n🛑 Agent stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()