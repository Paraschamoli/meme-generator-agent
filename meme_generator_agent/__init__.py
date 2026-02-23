# |---------------------------------------------------------|
# |                                                         |
# |                 Give Feedback / Get Help                |
# | https://github.com/getbindu/Bindu/issues/new/choose    |
# |                                                         |
# |---------------------------------------------------------|
#
#  Thank you users! We ❤️ you! - 🌻

"""meme-generator-agent - A Bindu Agent.

This agent uses browser automation to create memes on imgflip.com,
combining LLM capabilities with automated browser interactions.
"""

from meme_generator_agent.__version__ import __version__
from meme_generator_agent.main import handler, initialize_agent, main

__all__ = [
    "__version__",
    "handler",
    "initialize_agent",
    "main",
]
