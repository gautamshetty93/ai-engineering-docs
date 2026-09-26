# Day 5 — AI Engineering Toolchain, Testing & Project Structure

# 1. AI Applications Are Still Backend Applications

It is easy to think of an AI application as:

```text
User
 ↓
LLM API
 ↓
Answer
```

A real application is closer to:

```text
Client
   ↓
REST API
   ↓
Application / Business Logic
   ↓
LLM Client
   ↓
Model Provider
   ↓
OpenAI / Anthropic / Gemini
```

And eventually:

```text
Client
   ↓
FastAPI
   ↓
AI Service
   ├── LLM Client
   ├── Prompt Management
   ├── RAG
   ├── Vector Database
   ├── Agent Tools
   ├── Cache
   └── Database
         ↓
     LLM Provider
```

Therefore, traditional software-engineering principles remain extremely important.

LLMs add a new component to the architecture; they don't eliminate backend engineering.

---

# 2. Configuration Management

Applications behave differently depending on their environment.

For example:

```text
Development
Testing
Staging
Production
```

Configuration may include:

```text
LLM provider
Model name
API endpoint
API key
Database URL
Vector database URL
Temperature
Token limits
Timeout
Retry count
Logging level
```

These values should generally not be scattered throughout application code.

Bad design:

```python
model = "gpt-5"
timeout = 30
api_key = "secret-key"
```

Conceptually, configuration should be separated from application logic.

This is the same principle used by Spring Boot with:

```text
application.properties
application.yml
environment variables
Spring profiles
Vault
```

---

# 3. Secrets vs Configuration

An important distinction is:

```text
Configuration ≠ Secret
```

A model name such as:

```text
MODEL_NAME=gpt-5
```

is configuration.

An API key such as:

```text
OPENAI_API_KEY=...
```

is a **secret**.

Secrets include things such as:

- API keys
- Database passwords
- OAuth client secrets
- Access tokens
- Private keys

They should never be committed to source control.

---

# 4. What Is `.env`?

Python applications commonly use a `.env` file during local development.

Conceptually:

```text
.env
     ↓
Environment variables
     ↓
Application configuration
```

Example variables could be:

```text
OPENAI_API_KEY
ANTHROPIC_API_KEY
MODEL_NAME
DATABASE_URL
LOG_LEVEL
```

The application reads these values at runtime.

This separates:

```text
CODE
```

from:

```text
ENVIRONMENT-SPECIFIC CONFIGURATION
```

---

# 5. Why `.env` Should Not Be Committed

Suppose an API key gets committed to Git.

Even if you later delete the line, the key may remain in:

```text
Git history
Forks
Clones
CI logs
Caches
Backups
```

Therefore:

```text
.env
```

normally belongs in:

```text
.gitignore
```

If a secret accidentally reaches a public repository, deleting the file is not enough.

The credential should normally be **revoked/rotated**.

---

# 6. What Is `.env.example`?

Teams still need to know which configuration variables are required.

That's where:

```text
.env.example
```

is useful.

It contains the variable names but not the secrets.

Conceptually:

```text
.env.example

OPENAI_API_KEY=
ANTHROPIC_API_KEY=
MODEL_NAME=
```

This acts as documentation for developers.

So:

```text
.env          → real values → DON'T COMMIT

.env.example  → variable names/template → COMMIT
```

---

# 7. Secrets in Production

`.env` is convenient for local development.

It is usually not the ideal production secrets-management mechanism.

Production environments commonly use systems such as:

```text
AWS Secrets Manager
Azure Key Vault
Google Secret Manager
HashiCorp Vault
Kubernetes Secrets
CI/CD secret stores
```

The architecture becomes:

```text
Secret Manager
      ↓
Environment / Runtime
      ↓
Application
```

The application should not need to know exactly where the secret originally came from.

It simply consumes configuration exposed to its runtime environment.

This is very similar to how enterprise Spring applications handle secrets.

---

# 8. Python Project Structure

Python gives developers considerable freedom regarding project structure.

That flexibility can become problematic as projects grow.

A typical AI backend might conceptually contain:

```text
Application
│
├── API Layer
│
├── Models / Schemas
│
├── Services
│
├── LLM Clients
│
├── RAG
│
├── Configuration
│
├── Utilities
│
└── Tests
```

The goal is **separation of concerns**.

For example:

```text
API Layer
    ↓
AI Service
    ↓
LLM Client
    ↓
OpenAI / Anthropic
```

The FastAPI controller should not contain all of your prompt construction, provider logic, RAG logic and HTTP communication.

This is the same architectural principle used with:

```text
Controller
   ↓
Service
   ↓
Repository / Client
```

in Spring Boot.

---

# 9. Dependency Management

Python projects depend on external libraries just like Java applications.

Examples:

```text
FastAPI
Pydantic
httpx
pytest
OpenAI SDK
Anthropic SDK
LangChain
LlamaIndex
```

Java developers normally think in terms of:

```text
Maven / Gradle
        ↓
pom.xml / build.gradle
        ↓
dependencies
```

Python has multiple dependency-management approaches.

You may encounter:

```text
pip
requirements.txt
venv
uv
Poetry
pyproject.toml
```

The important principle is not memorizing every tool.

The principle is:

> Dependencies should be explicitly declared and reproducible.

Two developers checking out the same project should be able to create essentially the same environment.

---

# 10. Virtual Environments

Python dependencies are installed into a Python environment.

Without isolation, different projects can require incompatible versions.

For example:

```text
Project A
Pydantic 1.x

Project B
Pydantic 2.x
```

Installing everything globally can create conflicts.

Virtual environments solve this by creating isolated dependency environments.

Conceptually:

```text
Project A
   ↓
Virtual Environment A
   └── dependencies

Project B
   ↓
Virtual Environment B
   └── dependencies
```

The closest Java mental model is Maven/Gradle dependency isolation, although Python virtual environments operate differently.

---

# 11. Why Testing Matters Even More in AI Applications

AI applications contain two different categories of behavior.

### Deterministic behavior

Examples:

```text
Input validation
Authentication
Prompt construction
Database operations
Parsing
HTTP handling
Business rules
```

These can usually be tested with conventional software tests.

### Non-deterministic behavior

LLM output may vary.

For example:

```text
Prompt:
"Summarize this document."

Run 1:
"The document discusses..."

Run 2:
"This document primarily explains..."
```

Both could be correct.

Therefore, AI systems often require multiple testing strategies.

```text
Traditional Unit Tests
        +
Integration Tests
        +
LLM Evaluations
```

You will study evaluation techniques later.

For now, understand that **pytest primarily handles the normal software-engineering portion of your AI application**.

---

# 12. What Is pytest?

`pytest` is one of the most widely used testing frameworks in Python.

Your Java mental model can simply be:

```text
pytest ≈ JUnit
```

Both allow developers to verify expected application behavior automatically.

Typical test levels remain familiar:

```text
Unit Tests
Integration Tests
End-to-End Tests
```

AI does not change this testing pyramid fundamentally.

---

# 13. Unit Testing

A unit test verifies a small piece of application behavior independently.

Suppose:

```text
ChatService
     ↓
LLMClient
     ↓
OpenAI
```

If you're testing `ChatService`, you generally don't want every unit test to contact OpenAI.

Instead:

```text
ChatService
     ↓
Mock LLMClient
```

Now you're testing:

> Does my service behave correctly when the LLM client returns X?

rather than:

> Is OpenAI currently working correctly?

---

# 14. Why Mock External LLM Calls?

Real LLM API calls introduce several problems into unit tests.

### Cost

Every request may consume tokens and therefore money.

### Speed

A mocked response may take milliseconds.

A real LLM request may take seconds.

Imagine:

```text
500 tests × 2 seconds
```

Your test suite becomes unnecessarily slow.

### Reliability

Your test could fail because:

```text
Internet unavailable
Provider unavailable
Rate limit reached
API key expired
Timeout occurred
```

None of these necessarily mean your business logic is broken.

### Non-determinism

An LLM may produce different valid answers for the same prompt.

Traditional unit tests should ideally be deterministic.

Therefore:

```text
Unit Test
   ↓
Mock
   ↓
Known Response
```

---

# 15. Mocking Mental Model

As a Java developer, the easiest mapping is:

```text
Python mocking
      ≈
Mockito
```

Suppose your production architecture is:

```text
Service
   ↓
LLMClient
   ↓
HTTP Client
   ↓
OpenAI
```

For a unit test:

```text
Service
   ↓
LLMClient
   ↓
Mock HTTP Client
   ↓
Predefined Response
```

For example, conceptually:

```text
"When OpenAI returns 'Paris',
verify that my service correctly processes 'Paris'."
```

You control the dependency's behavior.

---

# 16. What Should We Test Around an LLM Client?

You generally don't test whether the LLM itself is intelligent.

You test **your code surrounding the model**.

Examples include:

```text
Was the correct model selected?

Was the prompt constructed correctly?

Was the API request constructed correctly?

Was authentication attached correctly?

Was the response parsed correctly?

What happens when the provider returns 429?

What happens on timeout?

What happens on 500?

What happens when the response is malformed?
```

This distinction is extremely important.

```text
Unit testing → test your code

Evaluation → test AI behavior/quality
```

These are related but different disciplines.

---

# 17. Testing Failure Scenarios

Production-quality systems must test more than successful responses.

LLM providers are external distributed systems.

Possible failures include:

```text
Timeout
429 Rate Limit
401 Authentication Failure
500 Provider Error
Network Failure
Invalid Response
Context Limit Exceeded
```

A robust AI service needs to decide:

```text
Should we retry?

Should we fail immediately?

Should we switch models?

Should we fall back to another provider?

Should we return a controlled error?
```

This will become increasingly important when you study production LLM architecture.

---

# 18. Code Formatting

Large teams need consistent code formatting.

Without automated formatting, developers waste time debating things such as:

```text
spacing
line wrapping
indentation
quotes
formatting
```

Python commonly uses automated formatters.

One popular formatter is:

```text
Black
```

Your mental model:

```text
Black ≈ Spotless
```

The key philosophy is:

> Formatting should be automated rather than debated during code reviews.

---

# 19. Linting

A linter analyzes source code for potential issues and style violations.

For Python, you'll commonly encounter:

```text
Ruff
```

It can detect many categories of problems such as:

```text
unused imports
unused variables
style problems
suspicious code patterns
import issues
```

Your rough Java mental model:

```text
Ruff
 ≈
Checkstyle + parts of static-analysis tooling
```

Formatting and linting are related but different.

```text
Formatter
    ↓
"How should this code look?"

Linter
    ↓
"Is there something suspicious or undesirable in this code?"
```

---

# 20. Why Docker Matters for AI Engineering

Your Python service may work perfectly on your laptop.

But production might use:

```text
Different Python version
Different OS
Different dependencies
Different system libraries
Different environment variables
```

The classic problem:

```text
"It works on my machine."
```

Containers help package:

```text
Application
+
Runtime
+
Dependencies
+
Configuration expectations
```

into a reproducible deployment unit.

---

# 21. Docker Image vs Container

This distinction remains important.

### Image

An image is an immutable package/template.

Think:

```text
Docker Image
=
Application blueprint
```

### Container

A container is a running instance of an image.

```text
Image
 ↓
Container 1

Image
 ↓
Container 2

Image
 ↓
Container 3
```

One image can therefore create many containers.

---

# 22. Dockerfile Mental Model

A `Dockerfile` describes how the application image should be constructed.

Conceptually:

```text
Choose Python runtime
       ↓
Create working directory
       ↓
Install dependencies
       ↓
Copy application
       ↓
Define startup command
```

For your FastAPI application:

```text
Docker Image
    ↓
Container
    ↓
Uvicorn
    ↓
FastAPI
    ↓
LLM Service
```

---

# 23. Never Bake Secrets Into Docker Images

A very important security principle:

```text
Docker Image
    ❌ API keys
    ❌ passwords
    ❌ tokens
```

Instead:

```text
Docker Image
      ↓
Container starts
      ↓
Secrets injected at runtime
      ↓
Application reads environment
```

This means the same image can be deployed to:

```text
Development
Staging
Production
```

with different configuration.

---

# 24. Reproducibility

A major goal of the entire Day 5 toolchain is **reproducibility**.

You want:

```text
Developer Laptop
      ↓
CI Pipeline
      ↓
Test Environment
      ↓
Production
```

to behave as consistently as possible.

Dependency management provides reproducible libraries.

Docker provides a reproducible runtime.

Tests provide reproducible verification.

Formatting/linting provides consistent source quality.

Configuration management separates code from environment-specific settings.

Together:

```text
Configuration
      +
Dependencies
      +
Testing
      +
Code Quality
      +
Containerization
      ↓
Reliable AI Service
```

---

# 25. Where This Fits in Future GenAI Development

The importance of this foundation becomes clearer when your architecture grows.

Eventually you may have:

```text
FastAPI
   ↓
AI Orchestration Layer
   ↓
┌──────────────────────────┐
│ LLM                      │
│ Embedding Model          │
│ Vector Database          │
│ RAG Pipeline             │
│ Reranker                 │
│ Agent Tools              │
│ External APIs            │
└──────────────────────────┘
```

Without good engineering practices, debugging such systems becomes extremely difficult.

You need to distinguish:

```text
Application bug?

Prompt problem?

LLM problem?

Retrieval problem?

External API problem?

Configuration problem?

Infrastructure problem?
```

Good project structure and testing make those boundaries clearer.

---
