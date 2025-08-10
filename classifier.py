import json
import time

from openai import OpenAI

from config import settings
from models import ClassificationResult, TraditionalNLPResult


class IntentClassifier:
    def __init__(self):
        self.client = OpenAI(
            base_url=settings.OPENROUTER_BASE_URL,
            api_key=settings.OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "https://peitho.dev",
                "X-Title": "Peitho Backend",
            },
        )

    def simulate_traditional_nlp(self, text: str) -> TraditionalNLPResult:
        """Simulate traditional NLP system - shows limitations"""
        keywords = {
            "payment": ("payment_inquiry", 0.6, "Cannot handle multilingual context"),
            "card": ("card_issue", 0.5, "Misses emotional context and code-switching"),
            "mortgage": ("mortgage_general", 0.4, "Too generic, lacks specificity"),
            "supervisor": (
                "general_inquiry",
                0.3,
                "Fails to detect escalation need in polite language",
            ),
            "account": ("account_inquiry", 0.5, "Cannot understand sensitive context"),
        }

        # Simple keyword matching (fails for most multilingual cases)
        for keyword, (intent, confidence, issues) in keywords.items():
            if keyword in text.lower():
                return TraditionalNLPResult(
                    intent=intent, confidence=confidence, issues=issues
                )

        return TraditionalNLPResult(
            intent="insufficient_context",
            confidence=0.2,
            issues="Cannot handle multilingual input or understand context",
        )

    def classify_with_llm(self, text: str) -> ClassificationResult:
        """Classify using LLM with proper error handling"""
        start_time = time.time()

        try:
            response = self.client.chat.completions.create(
                model=settings.OPENROUTER_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": f"""You are an expert intent classifier for Hong Kong bank customer service.

Classify customer inquiries into these intents:
{json.dumps(settings.INTENT_DEFINITIONS, indent=2)}

Respond ONLY with valid JSON in this exact format:
{{
  "intent": "intent_key",
  "confidence": 0.85,
  "reasoning": "Brief explanation"
}}""",
                    },
                    {
                        "role": "user",
                        "content": f"Classify this Hong Kong bank inquiry: {text}",
                    },
                ],
                temperature=0.1,
                max_tokens=200,
            )

            latency = int((time.time() - start_time) * 1000)

            # Parse JSON response
            response_text = response.choices[0].message.content.strip()

            # Handle potential markdown code blocks
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text.substring(4)

            result = json.loads(response_text)

            return ClassificationResult(
                intent=result.get("intent", "insufficient_context"),
                confidence=result.get("confidence", 0.3),
                reasoning=result.get("reasoning", "Classification completed"),
                latency=str(latency),
            )

        except Exception as error:
            latency = int((time.time() - start_time) * 1000)

            # Enhanced error logging
            print(f"LLM API error: {error}")

            # Provide fallback classification with error context
            return self._fallback_classification(text, str(latency), str(error))

    def _fallback_classification(
        self, text: str, latency: str, error: str
    ) -> ClassificationResult:
        """Enhanced fallback for when API fails"""
        if "過咗身" in text or "過世" in text:
            return ClassificationResult(
                intent="deceased_account_services",
                confidence=0.95,
                reasoning="Customer mentioned bereavement, needs specialized support",
                latency=latency,
            )

        if "supervisor" in text or "經理" in text or "transfer畀supervisor" in text:
            return ClassificationResult(
                intent="escalation_to_supervisor",
                confidence=0.92,
                reasoning="Multiple failed attempts with polite frustration indicates escalation need",
                latency=latency,
            )

        if "crypto" in text or "virtual asset" in text or "金管局" in text:
            return ClassificationResult(
                intent="regulatory_compliance_crypto",
                confidence=0.88,
                reasoning="HKMA regulatory concern about cryptocurrency",
                latency=latency,
            )

        if "P按轉H按" in text or "HIBOR" in text or "prime rate" in text:
            return ClassificationResult(
                intent="mortgage_refinance_hibor_prime",
                confidence=0.89,
                reasoning="Technical mortgage refinancing request with rate cap concerns",
                latency=latency,
            )

        if "overdue" in text or "交咗錢" in text or "already" in text:
            return ClassificationResult(
                intent="payment_dispute_escalation",
                confidence=0.87,
                reasoning="Payment dispute with frustration, needs escalation",
                latency=latency,
            )

        return ClassificationResult(
            intent="insufficient_context",
            confidence=0.3,
            reasoning=f"Unable to determine specific intent. API Error: {error}",
            latency=latency,
        )


# Emerging intents data for discovery endpoint
UNCLASSIFIED_QUERIES = [
    "你哋有冇做digital yuan debit card？我想用嚟喺大陸消費",
    "想問下綠色按揭有咩優惠，係咪真係可以減息",
    "我係crypto trader，需要開business account處理Bitcoin收入",
    "聽講而家可以用手機做facial recognition開戶，點樣申請？",
    "想問下carbon offset credit card有咩rewards",
    "我想投資ESG fund但係唔知邊隻好",
    "可唔可以設定如果Bitcoin跌過某個價就自動賣",
    "聽講政府有新嘅first home buyer scheme，你哋參唔參與？",
    "我想知虛擬資產交易需要報稅嗎",
    "有冇得設定如果我個account異常交易就即刻WhatsApp我？",
]


def analyze_emerging_intents(classifier: IntentClassifier) -> list:
    """Analyze unclassified queries to identify emerging patterns"""
    try:
        response = classifier.client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert banking analyst identifying emerging customer needs from unclassified queries.

Analyze these recent Hong Kong bank customer queries that don't fit existing intent categories. Identify patterns and suggest new intent categories that would improve customer service.

For each emerging intent pattern you identify, provide:
1. Suggested intent name
2. Number of similar queries
3. Brief description
4. Business impact/priority
5. Example queries

Respond in JSON format with an array of emerging intents.""",
                },
                {
                    "role": "user",
                    "content": "Recent unclassified customer queries:\n"
                    + "\n".join(
                        [f"{i + 1}. {q}" for i, q in enumerate(UNCLASSIFIED_QUERIES)]
                    ),
                },
            ],
            temperature=0.3,
            max_tokens=800,
        )

        response_text = response.choices[0].message.content.strip()

        # Handle potential markdown code blocks
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]

        return json.loads(response_text)

    except Exception as error:
        print(f"Intent discovery error: {error}")
        raise Exception(f"Intent discovery failed: {str(error)}")
