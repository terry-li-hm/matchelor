# Project Context for Claude

## Communication Preferences

Be direct, critical, and objective in feedback. Point out potential issues or better approaches honestly rather than just complying with requests. Provide honest assessments based on technical merit, prioritizing frankness over agreeability while remaining helpful and respectful. When something seems wrong, inefficient, or could be improved—say so directly. Don't hedge or soften criticism unnecessarily.

When writing documentation or explanations, prefer paragraph format over bulleted lists unless lists are specifically more suitable for the content. This applies to all written communication, including PR descriptions, GitHub issues, and conversational responses.

Proactively update this CLAUDE.md file when conversations reveal key insights that would significantly change how to approach the project in future sessions. Focus on context affecting strategy, constraints that limit options, or validated decisions that eliminate options. Skip exploratory discussions, implementation details, or observations that don't influence the approach.

Make atomic commits when features or significant functionality are complete rather than batching unrelated changes. Prefer frequent, small commits over larger ones when work can be divided into smaller, logical units that each deliver complete, working features.

Prioritize readable, self-explanatory code over comments. Write code that clearly expresses intent through meaningful variable names, function names, and structure. Comments should only exist when they provide essential context that cannot be expressed through the code itself.

Do not implement graceful fallbacks for LLM API failures in demo environments. When the LLM API fails, surface the actual error to stakeholders rather than hiding it behind fallback logic. This ensures real issues are visible and addressable during validation.

Maximize usage of shadcn/ui components throughout the frontend interface. Prefer shadcn/ui components over custom implementations to maintain design system consistency and leverage well-tested, accessible components.

Prefer browser-mcp tools over other browser automation tools when validating frontend functionality. Browser-mcp uses the user's actual browser session with existing authentication, cookies, and logged-in state, making it ideal for testing real-world scenarios without setup overhead.

## Project Overview

Peitho is an LLM-based intent classifier used in call centers. Named after the Greek goddess of persuasion and speech, it helps route customer calls by understanding caller intent. A demo is available at peitho.dev.

### Context

The user works at a bank in Hong Kong with direct access to validate use cases. The key differentiators for this project are handling multilingual code-switching among Cantonese, Mandarin, and English—which challenges traditional NLP systems—and emerging intent discovery that uncovers new customer patterns often missed by conventional NLP. The strategy is to validate internally with real stakeholders before considering external productization.
