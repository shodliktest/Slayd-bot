# 🎓 AI Slayd Bot - Professional Academic Content Generator

Professional Telegram bot for creating high-quality academic content using AI.

## ✨ Features

### 📊 PowerPoint Presentations
- Professional designs with multiple themes
- Automatic image integration
- Academic-quality content
- 5-50 slides support

### ✍️ Essays
- Academic writing style
- Structured format (Intro, Body, Conclusion)
- 500-5000 words
- Well-researched content

### ❓ Tests
- Multiple choice questions (4 options)
- Answer explanations
- Difficulty levels
- 10-100 questions

### 📝 Academic Papers
- **Referatlar** - Research papers with full structure
- **Mustaqil Ish** - Independent work assignments
- **Kurs Ishi** - Course projects (30+ pages)
- **Maqola** - Scientific articles for journals
- **Tezis** - Conference thesis papers

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Telegram Bot Token
- OpenAI API Key or Google Gemini API Key
- Telegram Channel for storage

### Installation

1. Clone the repository:
```bash
git clone https://github.com/shodliktest/Slayd-bot.git
cd Slayd-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:

Edit `.streamlit/secrets.toml`:

```toml
BOT_TOKEN = "your_bot_token"
ADMIN_IDS = "your_telegram_id"
STORAGE_CHANNEL_ID = "-1001234567890"

AI_PROVIDER = "groq"
GROQ_API_KEY = "gsk_your_groq_key"
GROQ_MODEL = "llama-3.1-70b-versatile"

SERPER_API_KEY = "your_serper_key"
UNSPLASH_ACCESS_KEY = "your_unsplash_key"
```

4. Run the bot:
```bash
python bot.py
```

5. Run admin panel (optional):
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
Slayd-bot/
├── bot.py                  # Main bot entry point
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── streamlit_app.py      # Admin web panel
├── handlers/             # Bot handlers
│   ├── start.py         # Welcome and main menu
│   ├── slide_creator.py # Presentation generator
│   ├── essay_creator.py # Essay writer
│   ├── test_creator.py  # Test generator
│   ├── referat_creator.py
│   ├── mustaqil_ish.py
│   ├── kurs_ishi.py
│   ├── maqola.py
│   └── tezis.py
├── keyboards/           # Inline keyboards
│   └── keyboards.py
├── utils/              # Utility modules
│   ├── ai_generator.py    # AI content generation
│   ├── pptx_generator.py  # PowerPoint creation
│   ├── web_search.py      # Web search & images
│   ├── tg_db.py          # Telegram storage
│   └── ram_cache.py      # Caching system
└── .streamlit/
    └── secrets.toml      # Configuration file
```

## 🎯 How It Works

### 1. User Interaction
- User selects content type from menu
- Bot asks for topic and parameters
- User provides details

### 2. Content Generation
- AI analyzes the topic
- Searches web for relevant information
- Finds appropriate images (for slides)
- Generates high-quality content

### 3. Delivery
- Creates formatted document (PPTX/TXT)
- Stores in Telegram channel (database)
- Sends to user with download options

## 🗄️ Database System

Uses **Telegram Channel as Database**:
- No external database needed
- Free and reliable
- Automatic backup
- Simple architecture

Data is stored as JSON files in a private Telegram channel:
- `index.json` - Main index (pinned)
- `slides_xxxxx.json` - Presentation data
- `essay_xxxxx.json` - Essay content
- `test_xxxxx.json` - Test data

## 🧠 AI Integration

### Supported Providers

**Groq (RECOMMENDED - Lightning Fast!):**
- Models: llama-3.1-70b, llama-3.1-8b, mixtral-8x7b
- Best for: All content types
- Speed: ⚡ 10x faster than GPT!
- Cost: 🆓 Free tier (generous limits)
- Get API: https://console.groq.com

**OpenAI GPT:**
- Models: gpt-4o, gpt-4o-mini, gpt-4-turbo
- Best for: All content types
- Cost: Pay per token
- Get API: https://platform.openai.com/api-keys

**Google Gemini:**
- Models: gemini-pro, gemini-pro-vision
- Best for: Long-form content
- Cost: Free tier available
- Get API: https://makersuite.google.com/app/apikey

### Content Quality

- Academic writing style
- Fact-checked information
- Proper structure and formatting
- Citations and references (when applicable)

## 🎨 Presentation Themes

- **Professional** - Corporate blue theme
- **Modern** - Clean and minimal
- **Academic** - Traditional scholarly style
- **Creative** - Vibrant and engaging

## 📊 Admin Panel Features

Streamlit web interface for:
- Real-time statistics
- User management
- Content monitoring
- System configuration
- Activity logs

Access: `http://localhost:8501`

## ⚙️ Configuration

### Bot Settings

```python
# config.py
MAX_SLIDES_PER_REQUEST = 50
MAX_ESSAY_WORDS = 5000
MAX_TEST_QUESTIONS = 100
DEFAULT_SLIDES_COUNT = 10
```

### Cache Settings

```python
RAM_CACHE_MAX_SIZE_MB = 450
CACHE_TTL_HOURS = 48
CLEANUP_INTERVAL_MINUTES = 15
```

## 🔒 Security

- Admin-only commands
- User authentication for admin panel
- API keys stored securely
- Private storage channel
- Rate limiting (can be added)

## 🚀 Deployment

### Local Development
```bash
python bot.py
```

### Production (systemd)

1. Create service file: `/etc/systemd/system/slayd-bot.service`

```ini
[Unit]
Description=AI Slayd Bot
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/Slayd-bot
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/python bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable slayd-bot
sudo systemctl start slayd-bot
```

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "bot.py"]
```

## 📝 API Keys Required

1. **Telegram Bot Token** - Free from [@BotFather](https://t.me/BotFather)
2. **Groq API Key** (RECOMMENDED) - FREE from https://console.groq.com
3. **OpenAI API Key** (optional) - https://platform.openai.com/api-keys
4. **Serper API** (optional) - https://serper.dev
5. **Unsplash API** (optional) - https://unsplash.com/developers

### 🚀 Why Groq?

- ⚡ **10x Faster** - Lightning speed responses
- 🆓 **Free Tier** - Generous limits
- 🎯 **High Quality** - Llama 3.1 70B model
- 💪 **Reliable** - Enterprise-grade infrastructure

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For questions and support:
- Telegram: @your_support
- Issues: GitHub Issues
- Email: your@email.com

## 🙏 Credits

- **AI**: OpenAI GPT / Google Gemini
- **Bot Framework**: aiogram 3.x
- **Presentation**: python-pptx
- **Web Panel**: Streamlit
- **Images**: Unsplash API

---

**Made with ❤️ for education and academic excellence**

🌟 Star this repository if you find it helpful!
