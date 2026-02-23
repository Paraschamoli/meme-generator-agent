"""Tests for the Meme Generator Agent."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from meme_generator_agent.main import handler, AgentResponse


@pytest.mark.asyncio
async def test_handler_returns_response():
    """Test that handler accepts messages and returns a properly formatted response."""
    messages = [{"role": "user", "content": "funny cat meme"}]
    expected_content = "### Here is your meme:\n\n![Generated Meme](https://i.imgflip.com/12345.jpg)"

    # Mock initialization to be already done
    # Mock generate_meme to return a string
    with patch("meme_generator_agent.main._initialized", True), \
         patch("meme_generator_agent.main.generate_meme", new_callable=AsyncMock, return_value=expected_content) as mock_gen:
        
        result = await handler(messages)

    # Verify result structure and content
    assert isinstance(result, AgentResponse)
    assert result.content == expected_content
    assert result.status == "COMPLETED"
    
    # Verify the generator was called with the correct query
    mock_gen.assert_called_once_with("funny cat meme")


@pytest.mark.asyncio
async def test_handler_extracts_last_user_message():
    """Test that handler processes multiple messages and uses the last user message."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "old query"},
        {"role": "assistant", "content": "response"},
        {"role": "user", "content": "actual query"},
    ]

    with patch("meme_generator_agent.main._initialized", True), \
         patch("meme_generator_agent.main.generate_meme", new_callable=AsyncMock, return_value="result") as mock_gen:
        
        await handler(messages)

    # Verify generate_meme was called with "actual query"
    mock_gen.assert_called_once_with("actual query")


@pytest.mark.asyncio
async def test_handler_initialization_flow():
    """Test that handler initializes the agent on the first call."""
    messages = [{"role": "user", "content": "Test"}]

    # Mock the Async Lock
    mock_lock_instance = MagicMock()
    mock_lock_instance.__aenter__ = AsyncMock(return_value=None)
    mock_lock_instance.__aexit__ = AsyncMock(return_value=None)

    with patch("meme_generator_agent.main._initialized", False), \
         patch("meme_generator_agent.main.initialize_agent", new_callable=AsyncMock) as mock_init, \
         patch("meme_generator_agent.main.generate_meme", new_callable=AsyncMock, return_value="content"), \
         patch("meme_generator_agent.main._init_lock", mock_lock_instance):
        
        await handler(messages)
        
        # Verify initialization was triggered
        mock_init.assert_called_once()


@pytest.mark.asyncio
async def test_handler_missing_user_query():
    """Test handler behavior when no user message is present."""
    messages = [{"role": "system", "content": "System only"}]

    with patch("meme_generator_agent.main._initialized", True):
        result = await handler(messages)

    assert "Please provide a description" in result.content