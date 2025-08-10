from pydantic import BaseModel


class ClassificationRequest(BaseModel):
    text: str


class ClassificationResult(BaseModel):
    intent: str
    confidence: float
    reasoning: str
    latency: str


class TraditionalNLPResult(BaseModel):
    intent: str
    confidence: float
    issues: str


class ClassificationResponse(BaseModel):
    traditional: TraditionalNLPResult
    llm: ClassificationResult


class EmergingIntent(BaseModel):
    name: str
    count: int
    description: str
    priority: str
    examples: list[str]
    businessImpact: str


class DiscoverResponse(BaseModel):
    emergingIntents: list[EmergingIntent]
    analysisDate: str
    totalUnclassifiedQueries: int
    analysisWindow: str


class HealthResponse(BaseModel):
    status: str
    api: dict | None = None
    environment: dict
    timestamp: str
    error: str | None = None
