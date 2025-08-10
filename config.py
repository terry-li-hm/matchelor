import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    # OpenRouter API configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_MODEL: str = "z-ai/glm-4.5-air"

    # API configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))

    # CORS configuration
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "https://peitho.dev",
        "https://peitho-demo.vercel.app",
    ]

    # Intent definitions for Hong Kong banking
    INTENT_DEFINITIONS = {
        "payment_dispute_escalation": "Customer reporting payment processing errors requiring immediate resolution",
        "escalation_to_supervisor": "Request for supervisor intervention due to unresolved issues",
        "passbook_fixed_deposit_inquiry": "Questions about traditional banking products (passbooks, fixed deposits)",
        "mortgage_refinance_hibor_prime": "Mortgage refinancing between HIBOR and Prime rate products",
        "deceased_account_services": "Account handling for deceased customers",
        "debit_card_application": "Application for ATM/debit card (not credit card)",
        "securities_margin_trading": "Stock trading with margin facilities",
        "security_lockout_escalation": "Multiple security-related failures requiring urgent attention",
        "wealth_management_trust_services": "High net worth services including trusts and estate planning",
        "regulatory_compliance_crypto": "Questions about cryptocurrency regulations and compliance",
        "remittance_limit_mainland": "Cross-border transfer limits to mainland China",
        "investment_linked_insurance_surrender": "ILAS product surrender and valuation",
        "sme_emergency_credit_facility": "Urgent business credit line requests",
        "fraud_verification_urgent": "Potential fraud in progress requiring immediate verification",
        "mpf_consolidation": "Mandatory Provident Fund scheme transfers",
        "insufficient_context": "Query too vague or lacks sufficient context for classification",
    }

    @classmethod
    def validate_environment(cls) -> bool:
        """Validate required environment variables"""
        if not cls.OPENROUTER_API_KEY:
            return False
        # Skip format validation if key appears to be masked/censored
        if cls.OPENROUTER_API_KEY.startswith("*"):
            return True
        if not cls.OPENROUTER_API_KEY.startswith("sk-or-v1-"):
            return False
        return True


# Create global settings instance
settings = Settings()
