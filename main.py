from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from classifier import IntentClassifier, analyze_emerging_intents
from config import settings
from logging_config import configure_logging, get_logger
from models import (
    ClassificationRequest,
    ClassificationResponse,
    DiscoverResponse,
    EmergingIntent,
    HealthResponse,
)

configure_logging()
logger = get_logger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Peitho - Hong Kong Bank Intent Classifier",
    description="LLM-based intent classification for multilingual call center routing",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize classifier
classifier = IntentClassifier()


@app.get("/")
async def root():
    return {
        "message": "Peitho Backend API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint with API connectivity test"""
    try:
        # Validate environment
        if not settings.validate_environment():
            return HealthResponse(
                status="unhealthy",
                environment={
                    "apiKeyConfigured": bool(settings.OPENROUTER_API_KEY),
                    "apiKeyFormat": "invalid"
                    if settings.OPENROUTER_API_KEY
                    and not settings.OPENROUTER_API_KEY.startswith("sk-or-v1-")
                    else "valid",
                },
                timestamp=datetime.now().isoformat(),
                error="Invalid environment variables: OPENROUTER_API_KEY (should start with 'sk-or-v1-')",
            )

        # Test API connection with minimal request
        start_time = datetime.now()
        test_result = classifier.classify_with_llm("Test")
        latency = int((datetime.now() - start_time).total_seconds() * 1000)

        return HealthResponse(
            status="healthy",
            api={
                "connected": True,
                "model": settings.OPENROUTER_MODEL,
                "latency": f"{latency}ms",
                "response": test_result.intent,
            },
            environment={
                "apiKeyConfigured": bool(settings.OPENROUTER_API_KEY),
                "apiKeyFormat": "valid",
            },
            timestamp=datetime.now().isoformat(),
        )

    except Exception as error:
        error_msg = str(error)

        # Provide specific troubleshooting hints
        if "No auth credentials found" in error_msg:
            error_msg += " - Check environment variables and restart server"

        if "401" in error_msg:
            error_msg += " - API key may be invalid or expired"

        return JSONResponse(
            status_code=500,
            content=HealthResponse(
                status="unhealthy",
                environment={
                    "apiKeyConfigured": bool(settings.OPENROUTER_API_KEY),
                    "apiKeyFormat": "valid"
                    if settings.OPENROUTER_API_KEY
                    and settings.OPENROUTER_API_KEY.startswith("sk-or-v1-")
                    else "invalid",
                },
                timestamp=datetime.now().isoformat(),
                error=error_msg,
            ).dict(),
        )


@app.post("/classify", response_model=ClassificationResponse)
async def classify_intent(request: ClassificationRequest):
    """Classify customer inquiry intent"""
    try:
        if not request.text or not request.text.strip():
            logger.warning("Empty text input received")
            raise HTTPException(status_code=400, detail="Text input is required")

        logger.info("Processing classification request", text_length=len(request.text))

        traditional = classifier.simulate_traditional_nlp(request.text)
        llm = classifier.classify_with_llm(request.text)

        logger.info(
            "Classification completed",
            llm_intent=llm.intent,
            llm_confidence=llm.confidence,
            latency=llm.latency,
        )

        return ClassificationResponse(traditional=traditional, llm=llm)

    except HTTPException:
        raise
    except Exception as error:
        logger.error("Classification failed", error=str(error))
        raise HTTPException(
            status_code=500, detail=f"Classification failed: {str(error)}"
        )


@app.get("/discover", response_model=DiscoverResponse)
async def discover_emerging_intents():
    """Discover emerging intents from unclassified queries"""
    try:
        emerging_intents_data = analyze_emerging_intents(classifier)

        # Convert to Pydantic models
        emerging_intents = []
        for intent_data in emerging_intents_data:
            emerging_intents.append(EmergingIntent(**intent_data))

        return DiscoverResponse(
            emergingIntents=emerging_intents,
            analysisDate=datetime.now().isoformat(),
            totalUnclassifiedQueries=127,
            analysisWindow="Last 30 days",
        )

    except Exception as error:
        raise HTTPException(
            status_code=500, detail=f"Intent discovery failed: {str(error)}"
        )


if __name__ == "__main__":
    print(f"🚀 Starting Peitho Backend on {settings.API_HOST}:{settings.API_PORT}")
    print(f"📊 Health check: http://{settings.API_HOST}:{settings.API_PORT}/health")
    print(f"📖 API docs: http://{settings.API_HOST}:{settings.API_PORT}/docs")

    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level="info",
    )
