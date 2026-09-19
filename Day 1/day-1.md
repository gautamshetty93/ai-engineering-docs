# Day 1 — LLM Fundamentals for an AI Engineer

# 1. What Is an LLM?

A **Large Language Model (LLM)** is a machine-learning model trained on very large amounts of text and other data.

Examples include models from OpenAI, Anthropic, Google, Meta, and others.

From an engineering perspective, you don't initially need to worry about exactly how billions of parameters were trained.

Think about the interface:

```text
Input
  ↓
Prompt / Messages
  ↓
Tokenization
  ↓
LLM
  ↓
Next-token generation
  ↓
Output text
```

For example:

```text
Input:

What is the capital of India?
```

The model generates something resembling:

```text
The → capital → of → India → is → New → Delhi
```

The important idea is that generation happens incrementally.

The model predicts a probability distribution for the **next token**, selects one, appends it to the existing sequence, and repeats.

---

# 2. Tokens and Tokenization

LLMs don't directly process text as words.

Text is converted into units called **tokens**.

For example:

```text
I love programming.
```

Conceptually, a tokenizer might represent it as:

```text
["I", " love", " programming", "."]
```

But tokens are **not necessarily words**.

A token can represent:

- An entire word
- Part of a word
- Punctuation
- Whitespace
- Symbols
- Parts of code

The exact tokenization depends on the model/tokenizer.

### Why should an AI Engineer care?

Because tokens directly affect:

```text
Cost
Latency
Context-window usage
Maximum output size
```

Suppose your request contains:

```text
Input: 10,000 tokens
Output: 2,000 tokens
```

Your API usage is roughly:

```text
Total processed/generated = 12,000 tokens
```

Providers generally report token usage in the API response or associated usage metrics.

This is similar to monitoring:

```text
Request size
Response size
Latency
CPU
Memory
Database queries
```

in traditional backend systems.

Token usage becomes another engineering metric.

---

# 3. Context Window

The **context window** is the amount of information the model can consider within a request.

Think of it as a limited working buffer.

Conceptually:

```text
Context Window
┌─────────────────────────────────────┐
│ System instructions                 │
│ Previous messages                   │
│ Retrieved documents                 │
│ Current user message                │
│ Generated response                  │
└─────────────────────────────────────┘
```

Different models support different context-window sizes.

A simplified constraint is:

```text
input tokens + generated tokens <= model/context limits
```

The exact API rules can differ between providers and models.

### Backend analogy

Imagine an API that accepts a request body with a maximum allowed payload.

If you exceed the allowed limit, you must reduce or restructure the data.

Similarly, AI applications often need strategies such as:

```text
Truncate old messages

OR

Summarize previous messages

OR

Retrieve only relevant information

OR

Store information externally
```

These ideas eventually lead to architectures involving:

- Conversation stores
- Summarization
- Vector databases
- RAG
- Semantic search
- Long-term memory

We will encounter these later.

---

# 4. Autoregressive Generation

Most chat-oriented LLMs generate responses **autoregressively**.

That means:

> Generate one token, add it to the existing sequence, then use the updated sequence to generate the next token.

Example:

```text
Prompt:

Java is a
```

The model might predict:

```text
programming
```

Now the sequence becomes:

```text
Java is a programming
```

Then it predicts another token:

```text
language
```

Now:

```text
Java is a programming language
```

The cycle continues until the model reaches a stopping condition.

Conceptually:

```text
Prompt
  ↓
Predict next token
  ↓
Append token
  ↓
Predict next token
  ↓
Append token
  ↓
...
  ↓
Stop
```

This explains an important characteristic of LLM latency.

Generating 1,000 output tokens requires substantially more sequential generation work than generating 10 output tokens.

Therefore:

```text
More output tokens
      ↓
More generation work
      ↓
Usually higher latency + higher cost
```

---

# 5. Temperature

The model doesn't simply have one possible next token.

Internally, candidate tokens have probabilities.

Simplified example:

```text
"The capital of India is..."

New Delhi    0.94
Delhi        0.04
Mumbai       0.01
Other        0.01
```

**Temperature** influences how the model samples from those possibilities.

Conceptually:

### Lower temperature

```text
More deterministic
More predictable
Less variation
```

Useful for things such as:

- Data extraction
- Classification
- Structured responses
- Some coding tasks

### Higher temperature

```text
More variation
More randomness
More diverse outputs
```

Potentially useful for:

- Brainstorming
- Creative writing
- Generating alternatives

Important:

> Temperature does not make the model "smarter."

It changes the sampling behavior.

---

# 6. Top-p

**Top-p** is another sampling control.

Instead of considering every possible next token, nucleus sampling considers a set of likely tokens whose cumulative probability reaches a threshold.

For example:

```text
Token A    50%
Token B    25%
Token C    15%
Token D     5%
Token E     5%
```

With:

```text
top_p = 0.90
```

the sampling pool might roughly contain:

```text
A + B + C
```

because:

```text
50% + 25% + 15% = 90%
```

You generally don't need to constantly tune both temperature and top-p.

The important Day-1 understanding is:

```text
Temperature → controls randomness

Top-p → controls the candidate probability mass considered
```

---

# 7. The Most Important Mental Model

As a backend engineer, think of an LLM API like this:

```text
Client
   ↓
POST /model
   ↓
JSON Request
   ↓
LLM inference
   ↓
JSON Response
```

Conceptually:

```http
POST /model
Content-Type: application/json
Authorization: Bearer <API_KEY>
```

Request:

```json
{
  "model": "some-model",
  "messages": [
    {
      "role": "user",
      "content": "Explain Kafka in simple terms."
    }
  ]
}
```

Response:

```json
{
  "output": "...",
  "usage": {
    "input_tokens": 10,
    "output_tokens": 100
  }
}
```

You've dealt with this architecture many times before.

The interesting engineering problems appear around the model.

---

# 8. LLM APIs Are Stateless

This is one of the most important concepts for building AI applications.

Imagine this conversation:

```text
User:
My name is John.

Assistant:
Nice to meet you, John.
```

Then another request:

```text
User:
What is my name?
```

How does the model know?

The application typically sends relevant previous conversation information again.

Conceptually:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "My name is John."
    },
    {
      "role": "assistant",
      "content": "Nice to meet you, John."
    },
    {
      "role": "user",
      "content": "What is my name?"
    }
  ]
}
```

The model isn't necessarily remembering the previous REST request.

Your **application manages the state**.

This should feel familiar.

A backend system might use:

```text
Client
   ↓
REST API
   ↓
Application
   ↓
Redis / Database
```

An AI application might use:

```text
User
   ↓
Chat API
   ↓
AI Application
   ↓
Conversation DB
   ↓
Construct context
   ↓
LLM API
```

The application retrieves the relevant state and supplies it to the model.

---

# 9. Where AI Engineering Begins

Calling an LLM API is easy.

Building a reliable system around it is the actual engineering challenge.

An AI Engineer may build systems involving:

```text
Application
     ↓
Prompt construction
     ↓
LLM
     ↓
Structured output
     ↓
Validation
```

More advanced applications might look like:

```text
User
 ↓
Backend API
 ↓
Authentication
 ↓
Conversation Manager
 ↓
RAG / Retrieval
 ↓
Vector Database
 ↓
Prompt Builder
 ↓
LLM
 ↓
Tool Calling
 ↓
External APIs
 ↓
Response Validation
 ↓
Observability
 ↓
User
```

Notice something important:

**Most of this is software engineering.**

Your existing backend knowledge remains extremely useful.

Concepts such as:

- REST
- Microservices
- Authentication
- Databases
- Caching
- Kafka
- Distributed systems
- Observability
- Docker
- Cloud
- CI/CD

continue to matter.

You're adding LLMs as another powerful component in the architecture.

---

# 10. AI Engineer vs ML Engineer vs Research Scientist

These roles overlap, and companies use the titles differently, but a useful general distinction is:

| Role               | Primary Focus                                            |
| ------------------ | -------------------------------------------------------- |
| AI Engineer        | Build applications/systems using AI models               |
| ML Engineer        | Train, deploy, evaluate, and operate ML models/pipelines |
| Research Scientist | Develop and investigate new model techniques/algorithms  |

### AI Engineer

Typical work:

```text
LLM APIs
RAG
Vector databases
Prompt engineering
Agents
Tool calling
Evaluation
Guardrails
AI application architecture
Observability
Backend integration
```

Example:

> Build a customer-support assistant that searches company documentation and answers questions using an LLM.

---

### ML Engineer

Typical work can include:

```text
Training pipelines
Data pipelines
Feature engineering
Model evaluation
Fine-tuning
Model serving
MLOps
GPU infrastructure
Experiment tracking
```

Example:

> Train and deploy a recommendation model using customer interaction data.

---

### Research Scientist

Typical work can involve:

```text
Model architectures
Training techniques
Optimization
Research experiments
Mathematics
Research papers
Novel algorithms
```

Example:

> Develop a new attention mechanism and evaluate whether it improves model performance.

These boundaries are not absolute. Real jobs can combine responsibilities.

---

# 11. The LLM Request Lifecycle

When your application calls an LLM API, think about the complete lifecycle.

```text
1. Application creates prompt/messages
              ↓
2. Request is serialized
              ↓
3. HTTPS request reaches provider
              ↓
4. Input is tokenized
              ↓
5. Model performs inference
              ↓
6. Tokens are generated autoregressively
              ↓
7. Output is returned
              ↓
8. Application parses response
              ↓
9. Usage/latency is recorded
```

As an AI Engineer, you'll eventually monitor metrics such as:

```text
Input tokens
Output tokens
Latency
Time to first token
Cost
Errors
Rate limits
Model/provider
Quality/evaluation metrics
```

Think of this as normal API observability with several AI-specific metrics added.

---
