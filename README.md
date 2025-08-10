# Peitho Backend API

LLM-based intent classification for Hong Kong banking call centers.

## Local Development

```bash
# Install dependencies with uv
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your actual OPENROUTER_API_KEY

# Run the server
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard:
   - `OPENROUTER_API_KEY` (your OpenRouter API key)
3. Deploy automatically via Git push

Railway configuration is in `railway.json`.

## API Endpoints

- `GET /` - API info
- `GET /health` - Health check with API connectivity test
- `POST /classify` - Intent classification
- `GET /discover` - Emerging intent discovery
- `GET /docs` - Swagger API documentation
