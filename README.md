<p align="center">
  <img src="https://raw.githubusercontent.com/getbindu/create-bindu-agent/refs/heads/main/assets/light.svg" alt="bindu Logo" width="200">
</p>

<h1 align="center">Meme Generator Agent</h1>
<h3 align="center">AI-Powered Meme Creation with Browser Automation</h3>

<p align="center">
  <strong>Intelligent meme generation combining AI context understanding with automated browser interactions</strong><br/>
  Create contextually relevant memes with witty captions using advanced template selection and humor analysis
</p>

<p align="center">
  <a href="https://github.com/Paraschamoli/meme-generator-agent/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/Paraschamoli/meme-generator-agent/main.yml?branch=main" alt="Build Status">
  </a>
  <a href="https://pypi.org/project/meme-generator-agent/">
    <img src="https://img.shields.io/pypi/v/meme-generator-agent" alt="PyPI Version">
  </a>
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="Python Version">
  <a href="https://github.com/Paraschamoli/meme-generator-agent/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/Paraschamoli/meme-generator-agent" alt="License">
  </a>
</p>

---

## 🎯 What is Meme Generator Agent?

An AI-powered meme creation assistant that combines intelligent context understanding with automated browser interactions to generate contextually relevant, humorous memes. Think of it as having a professional meme creator with perfect timing and wit available 24/7.

### Key Features

- **🤖 Intelligent Template Selection** - AI analyzes prompts to select the perfect meme template
- **🌐 Browser Automation** - Direct interaction with meme generation platforms via browser_use
- **💬 Witty Caption Generation** - Context-aware humor creation with multiple tone options
- **⚡ High-Quality Output** - Optimized text positioning and readability
- **🔄 Lazy Initialization** - Fast boot times, initializes on first request
- **🔐 Secure API Handling** - No API keys required at startup

---

## 🛠️ Tools & Capabilities

### Built-in Technologies

- **Browser Use Framework** - Advanced browser automation and interaction
- **OpenAI/OpenRouter Integration** - State-of-the-art AI for context analysis
- **ImgFlip Platform** - Direct meme generation through web automation

### Meme Generation Methodology

1.  **Context Analysis** - Understand the prompt, emotion, and target audience
2.  **Template Selection** - AI chooses from 1000+ templates based on contextual relevance
3.  **Caption Creation** - Generate witty, contextually appropriate top/bottom text
4.  **Quality Optimization** - Optimize text size, positioning, and readability
5.  **Output Generation** - Produce high-quality meme with direct link

---

> **🌐 Join the Internet of Agents**
> Register your agent at [bindus.directory](https://bindus.directory) to make it discoverable worldwide and enable agent-to-agent collaboration. It takes 2 minutes and unlocks the full potential of your agent.

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ParasChamoli/meme-generator-agent.git
cd meme-generator-agent

# Set up virtual environment with uv
uv venv --python 3.12
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv sync

# Install browser dependencies
uv run playwright install chromium
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API key (choose one):
# OPENAI_API_KEY=sk-...      # For OpenAI GPT-4o
# OPENROUTER_API_KEY=sk-...  # For OpenRouter (cheaper alternative)
```

### 3. Run Locally

```bash
# Start the meme generator agent
uv run python -m meme_generator_agent

# Agent will be available at http://localhost:3773
```

### 4. Test with Docker

```bash
# Build and run with Docker Compose
docker-compose up --build

# Access at: http://localhost:3773
```

---

## � Configuration

### Environment Variables

Create a `.env` file:

```env
# Choose ONE provider (both can be set, OpenAI takes priority)
OPENAI_API_KEY=sk-...      # OpenAI API key
OPENROUTER_API_KEY=sk-...  # OpenRouter API key (alternative)

# Optional
MODEL_NAME=gpt-4o          # Model selection
DEBUG=true                 # Enable debug logging
```

### Port Configuration

Default port: `3773` (can be changed in `agent_config.json`)

---

## 💡 Usage Examples

### Via HTTP API

```bash
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {
        "role": "user",
        "content": "Create a meme about when your code finally works after 100 attempts"
      }
    ]
  }'
```

### Sample Meme Queries

```text
"Generate a meme about Monday morning coffee addiction"
"Create a meme showing the struggle of learning to code"
"Make a meme about procrastination and deadlines"
"Generate a meme about the difference between expectations and reality in programming"
```

### Expected Output Format

```markdown
### Here is your meme:

![Generated Meme](https://i.imgflip.com/abc123.jpg)

[View on ImgFlip](https://imgflip.com/i/abc123)
```

---

## � Docker Deployment

### Quick Docker Setup

```bash
# Build the image
docker build -t meme-generator-agent .

# Run container
docker run -d \
  -p 3773:3773 \
  -e OPENAI_API_KEY=your_key_here \
  --name meme-generator-agent \
  meme-generator-agent

# Check logs
docker logs -f meme-generator-agent
```

### Docker Compose (Recommended)

**docker-compose.yml**

```yaml
version: "3.8"
services:
  meme-generator-agent:
    build: .
    ports:
      - "3773:3773"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    restart: unless-stopped
```

**Run with Compose:**

```bash
# Start with compose
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 📁 Project Structure

```text
meme-generator-agent/
├── meme_generator_agent/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Main agent implementation
│   └── skills/
│       └── meme-generator/
│           ├── skill.yaml   # Skill configuration
│           └── __init__.py
├── agent_config.json        # Bindu agent configuration
├── pyproject.toml           # Python dependencies
├── Dockerfile               # Multi-stage Docker build
├── docker-compose.yml       # Docker Compose setup
├── README.md                # This documentation
├── .env.example             # Environment template
└── uv.lock                  # Dependency lock file
```

---

## 🔌 API Reference

### Health Check

```bash
GET http://localhost:3773/health
```

**Response:**

```json
{ "status": "healthy", "agent": "Meme Generator Agent" }
```

### Chat Endpoint

```bash
POST http://localhost:3773/chat
Content-Type: application/json

{
  "messages": [
    {"role": "user", "content": "Create a meme about programming struggles"}
  ]
}
```

---

## 🧪 Testing

### Local Testing

```bash
# Install test dependencies
uv sync --group dev

# Run tests
pytest tests/

# Test with specific API key
OPENAI_API_KEY=test_key python -m pytest
```

### Integration Test

```bash
# Start agent
python meme_generator_agent/main.py &

# Test API endpoint
curl -X POST http://localhost:3773/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Test meme generation"}]}'
```

---

## � Troubleshooting

### Common Issues & Solutions

- **"ModuleNotFoundError"**

  ```bash
  uv sync --force
  ```

- **"Port 3773 already in use"**
  Change port in `agent_config.json` or kill the process:

  ```bash
  lsof -ti:3773 | xargs kill -9
  ```

- **"No API key provided"**
  Check if `.env` exists and variable names match. Or set directly:

  ```bash
  export OPENAI_API_KEY=your_key
  ```

- **Browser automation fails**

  ```bash
  # Reinstall Playwright browsers
  uv run playwright install chromium
  ```

- **Docker build fails**
  ```bash
  docker system prune -a
  docker-compose build --no-cache
  ```

---

## 📊 Dependencies

### Core Packages

- `bindu` - Agent deployment framework
- `browser-use` - Browser automation framework
- `langchain-openai` - OpenAI client integration
- `playwright` - Browser automation engine
- `python-dotenv` - Environment management
- `requests` - HTTP requests

### Development Packages

- `pytest` - Testing framework
- `ruff` - Code formatting/linting
- `pre-commit` - Git hooks
- `ty` - Type checking

---

## 🎯 Skills

### meme-generator (v1.0.0)

**Primary Capability:**

- Intelligent meme generation using browser automation
- Context-aware template selection and caption creation
- High-quality output with optimized text positioning

**Features:**

- 1000+ template database with intelligent selection
- Multiple humor styles (witty, sarcastic, relatable)
- Browser automation for direct platform interaction
- Quality optimization for readability and visual appeal

**Best Used For:**

- Social media content creation
- Humorous takes on situations
- Expressing ideas through visual humor
- Marketing and engagement content

**Not Suitable For:**

- Serious or formal content
- Complex data visualization
- Academic or technical documentation
- Real-time news reporting

**Performance:**

- Average processing time: ~45 seconds
- Max concurrent requests: 3
- Memory per request: 512MB
- Success rate: 92%

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1.  **Fork** the repository
2.  **Create** a feature branch: `git checkout -b feature/improvement`
3.  **Make your changes** following the code style
4.  **Add tests** for new functionality
5.  **Commit** with descriptive messages
6.  **Push** to your fork
7.  **Open** a Pull Request

**Code Style:**

- Follow PEP 8 conventions
- Use type hints where possible
- Add docstrings for public functions
- Keep functions focused and small

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits & Acknowledgments

- **Developer:** Paras Chamoli
- **Framework:** [Bindu](https://bindus.directory) - Agent deployment platform
- **Browser Automation:** [Browser Use](https://github.com/browser-use/browser-use) - Web automation framework
- **Meme Platform:** [ImgFlip](https://imgflip.com) - Meme generation platform

### 🔗 Useful Links

- 🌐 **Bindu Directory:** [bindus.directory](https://bindus.directory)
- 📚 **Bindu Docs:** [docs.getbindu.com](https://docs.getbindu.com)
- � **GitHub:** [github.com/ParasChamoli/meme-generator-agent](https://github.com/ParasChamoli/meme-generator-agent)
- 💬 **Discord:** Bindu Community

<br>

<p align="center">
  <strong>Built with ❤️ by Paras Chamoli</strong><br/>
  <em>Transforming humor creation with AI-powered meme generation</em>
</p>

<p align="center">
  <a href="https://github.com/ParasChamoli/meme-generator-agent/stargazers">⭐ Star on GitHub</a> •
  <a href="https://bindus.directory">🌐 Register on Bindu</a> •
  <a href="https://github.com/ParasChamoli/meme-generator-agent/issues">🐛 Report Issues</a>
</p>

> **Note:** This agent follows the Bindu pattern with lazy initialization and secure API key handling. It boots without API keys and only fails at runtime if keys are needed but not provided.
