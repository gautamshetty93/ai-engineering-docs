# Day 3 — Python for AI Engineers, Part 1

# 1. Python vs Java — Mental Model

Since we already understand Java, the fastest way to learn Python is to map familiar Java concepts to their Python equivalents.

| Java                                    | Python                      |
| --------------------------------------- | --------------------------- |
| Maven / Gradle                          | `uv`, `pip`                 |
| Maven project dependency isolation      | Virtual environment         |
| `String` / `Integer` / `List<String>`   | `str` / `int` / `list[str]` |
| Static types                            | Type hints                  |
| POJO                                    | `dataclass`                 |
| DTO                                     | Pydantic `BaseModel`        |
| `String.format()`                       | f-string                    |
| Streams                                 | Comprehensions              |
| try-with-resources                      | `with`                      |
| `HttpClient` / RestTemplate / WebClient | `httpx`                     |
| Jackson                                 | Pydantic                    |
| `pom.xml` / `build.gradle`              | `pyproject.toml`            |
| JVM                                     | Python interpreter          |

The important difference is that Python is **dynamically typed**.

Java:

```java
String name = "GPT";
int tokens = 100;
```

Python:

```python
name = "GPT"
tokens = 100
```

Python determines the types at runtime.

However, modern Python applications frequently use **type hints** to make code easier to understand and maintain.

```python
name: str = "GPT"
tokens: int = 100
```

This should feel much more natural to a Java developer.

---

# 2. Virtual Environments

## What problem do virtual environments solve?

Suppose Project A requires:

```text
pydantic 2.x
```

while Project B requires a different dependency version.

Installing everything globally can create dependency conflicts.

Python solves this using **virtual environments**.

Think of a virtual environment as:

> A dependency-isolated Python environment belonging to one project.

Conceptually:

```text
Java
Project
 └── pom.xml
      └── project dependencies

Python
Project
 └── .venv
      └── project dependencies
```

---

# 3. Creating a Virtual Environment with `venv`

Create a project directory:

```bash
mkdir day-03-python
cd day-03-python
```

Create the environment:

```bash
python -m venv .venv
```

The directory will now look roughly like:

```text
day-03-python/
└── .venv/
```

### Activate it

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

After activation, the terminal usually shows:

```text
(.venv)
```

Install dependencies:

```bash
pip install httpx pydantic
```

Check installed packages:

```bash
pip list
```

Deactivate the environment:

```bash
deactivate
```

---

# 4. Using `uv`

`uv` is a modern Python package and project manager.

For an AI engineering project, it can provide a convenient workflow for:

- creating projects
- managing virtual environments
- installing dependencies
- maintaining dependency metadata

Create a project:

```bash
uv init day-03-python
cd day-03-python
```

Add dependencies:

```bash
uv add httpx pydantic
```

Run Python:

```bash
uv run python
```

Run a script:

```bash
uv run python main.py
```

A typical project may look like:

```text
day-03-python/
├── .venv/
├── main.py
├── pyproject.toml
└── uv.lock
```

### Java analogy

Think approximately:

```text
pyproject.toml
```

as playing a role similar to:

```text
pom.xml
```

or:

```text
build.gradle
```

It isn't an exact one-to-one mapping, but it is a useful mental model.

---

# 5. Python Type Hints

Without type hints:

```python
def greet(name):
    return "Hello " + name
```

With type hints:

```python
def greet(name: str) -> str:
    return "Hello " + name
```

Java equivalent:

```java
String greet(String name) {
    return "Hello " + name;
}
```

Another example:

```python
def add(a: int, b: int) -> int:
    return a + b
```

Collections:

```python
def get_models() -> list[str]:
    return [
        "gpt-5",
        "claude-sonnet",
        "gemini"
    ]
```

Dictionary:

```python
def get_usage() -> dict[str, int]:
    return {
        "input_tokens": 100,
        "output_tokens": 50
    }
```

### Important

Python type hints generally **do not enforce types at runtime**.

This is valid Python:

```python
def add(a: int, b: int) -> int:
    return a + b
```

The annotations primarily help:

- developers
- IDEs
- static type checkers
- documentation
- code maintainability

This differs significantly from Java's compile-time type system.

---

# 6. f-Strings

Java developers often construct strings using concatenation:

```java
String message = "Hello " + name;
```

Python supports f-strings:

```python
name = "GPT"

message = f"Hello {name}"

print(message)
```

Output:

```text
Hello GPT
```

Expressions can also be embedded.

```python
input_tokens = 100
output_tokens = 50

print(f"Total tokens: {input_tokens + output_tokens}")
```

Output:

```text
Total tokens: 150
```

f-strings are extremely common in Python.

---

# 7. List Comprehensions

Suppose we have:

```python
numbers = [1, 2, 3, 4, 5]
```

Traditional loop:

```python
squares = []

for number in numbers:
    squares.append(number * number)
```

Python comprehension:

```python
squares = [number * number for number in numbers]
```

Result:

```text
[1, 4, 9, 16, 25]
```

Filtering can also be included:

```python
even_numbers = [
    number
    for number in numbers
    if number % 2 == 0
]
```

Result:

```text
[2, 4]
```

For a Java developer, comprehensions can loosely be compared to simple Stream operations.

Java:

```java
List<Integer> squares =
    numbers.stream()
           .map(n -> n * n)
           .toList();
```

Python:

```python
squares = [n * n for n in numbers]
```

---

# 8. Dictionary Comprehensions

Python can also construct dictionaries using comprehensions.

```python
models = ["gpt", "claude", "gemini"]

model_lengths = {
    model: len(model)
    for model in models
}
```

Result:

```python
{
    "gpt": 3,
    "claude": 6,
    "gemini": 6
}
```

This pattern appears frequently when transforming API responses and datasets.

---

# 9. Context Managers — `with`

Java provides try-with-resources:

```java
try (BufferedReader reader = new BufferedReader(...)) {
    // use resource
}
```

Python uses context managers:

```python
with open("data.txt", "r") as file:
    content = file.read()
```

When the block finishes, Python automatically closes the resource.

Conceptually:

```text
Java try-with-resources
        ↓
Python with
```

Context managers are commonly used with:

- files
- network clients
- database connections
- locks
- transactions

---

# 10. Dataclasses

Suppose we want to represent an LLM request.

Using a normal Python class:

```python
class LLMRequest:

    def __init__(self, model: str, prompt: str):
        self.model = model
        self.prompt = prompt
```

Python provides `dataclass` to reduce boilerplate.

```python
from dataclasses import dataclass


@dataclass
class LLMRequest:
    model: str
    prompt: str
```

Usage:

```python
request = LLMRequest(
    model="my-model",
    prompt="Explain vector databases"
)

print(request.model)
print(request.prompt)
```

This is similar to a simple Java POJO or record.

---

# 11. Pydantic Models

For AI/backend engineering, **Pydantic** is particularly important.

Pydantic lets us define structured models and validate incoming data.

Install it:

```bash
pip install pydantic
```

Example:

```python
from pydantic import BaseModel


class LLMRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 0.7
```

Create an object:

```python
request = LLMRequest(
    model="my-model",
    prompt="Explain RAG"
)
```

Convert it into a dictionary:

```python
print(request.model_dump())
```

Example result:

```python
{
    "model": "my-model",
    "prompt": "Explain RAG",
    "temperature": 0.7
}
```

Convert to JSON:

```python
print(request.model_dump_json())
```

---

# 12. Pydantic vs Java DTO

Java:

```java
public class LLMRequest {

    private String model;
    private String prompt;
    private double temperature;

}
```

Python:

```python
from pydantic import BaseModel


class LLMRequest(BaseModel):
    model: str
    prompt: str
    temperature: float = 0.7
```

A useful mental model is:

```text
Pydantic Model
      ≈
Java DTO + validation + JSON serialization/deserialization
```

This is why Pydantic appears frequently in modern Python API and AI applications.

---

# 13. Making HTTP Requests with `httpx`

Install:

```bash
pip install httpx
```

Basic GET request:

```python
import httpx


response = httpx.get("https://example.com")

print(response.status_code)
print(response.text)
```

POST request:

```python
import httpx


payload = {
    "model": "my-model",
    "prompt": "Explain embeddings"
}

response = httpx.post(
    "https://example.com/api",
    json=payload
)

print(response.status_code)
print(response.json())
```

For a Java developer, think of `httpx` as serving a similar purpose to HTTP clients such as:

```text
Java HttpClient
RestTemplate
WebClient
OkHttp
```

---

# 14. Typed API Requests with Pydantic

Now combine Pydantic and `httpx`.

```python
import httpx
from pydantic import BaseModel


class LLMRequest(BaseModel):
    model: str
    prompt: str


class LLMResponse(BaseModel):
    response: str


def call_llm(request: LLMRequest) -> LLMResponse:

    response = httpx.post(
        "https://example.com/llm",
        json=request.model_dump()
    )

    response.raise_for_status()

    return LLMResponse.model_validate(
        response.json()
    )
```

Usage:

```python
request = LLMRequest(
    model="my-model",
    prompt="Explain vector databases"
)

result = call_llm(request)

print(result.response)
```

The architecture should look very familiar:

```text
Caller
   │
   ▼
LLMRequest DTO
   │
   ▼
HTTP Client
   │
   ▼
LLM API
   │
   ▼
JSON Response
   │
   ▼
LLMResponse DTO
```

This is essentially the same pattern used when building REST integrations in Java.

---

# 15. Rewrite the Day 1 `curl` Call in Python

On Day 1 we called an LLM API using `curl`.

Conceptually:

```bash
curl POST /messages
```

Today we replace that with:

```text
Python
   ↓
Pydantic Request Model
   ↓
httpx
   ↓
LLM REST API
   ↓
JSON
   ↓
Pydantic Response Model
```

Example structure:

```python
import os

import httpx
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class LLMRequest(BaseModel):
    model: str
    messages: list[Message]


class LLMClient:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(self, request: LLMRequest) -> dict:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        with httpx.Client(timeout=30.0) as client:

            response = client.post(
                "https://example.com/v1/messages",
                headers=headers,
                json=request.model_dump()
            )

            response.raise_for_status()

            return response.json()


api_key = os.environ["LLM_API_KEY"]

client = LLMClient(api_key)

request = LLMRequest(
    model="your-model",
    messages=[
        Message(
            role="user",
            content="Explain embeddings in simple terms."
        )
    ]
)

response = client.generate(request)

print(response)
```

> The endpoint and payload format above are intentionally generic. When calling a real provider, use that provider's current API endpoint and request/response schema.

---

# 16. Why Use `with httpx.Client()`?

Notice:

```python
with httpx.Client() as client:
```

This is our context manager.

It is conceptually similar to:

```java
try (SomeResource client = ...) {

}
```

Python automatically cleans up the client when execution leaves the block.

This gives us another example of:

```text
Java try-with-resources
          ↓
Python context manager
          ↓
with
```

---

# 17. API Keys — Never Hardcode Secrets

Do **not** write:

```python
api_key = "sk-secret-key"
```

Especially if the project will be pushed to GitHub.

Instead, use an environment variable.

Windows PowerShell:

```powershell
$env:LLM_API_KEY="your-api-key"
```

macOS/Linux:

```bash
export LLM_API_KEY="your-api-key"
```

Then:

```python
import os

api_key = os.environ["LLM_API_KEY"]
```

Also add environment files to `.gitignore` if you use them:

```gitignore
.venv/
.env
__pycache__/
*.pyc
```

Never commit API keys to GitHub.

---

# 18. Recommended Project Structure

A simple Day 3 project could look like:

```text
day-03-python/
│
├── README.md
├── pyproject.toml
├── uv.lock
├── .gitignore
│
└── src/
    ├── main.py
    ├── models.py
    └── llm_client.py
```

Responsibilities:

```text
models.py
    ↓
Pydantic request/response models

llm_client.py
    ↓
HTTP communication with LLM APIs

main.py
    ↓
Application entry point
```

This is conceptually similar to:

```text
Java

dto/
service/
controller/
```

The Python version simply tends to use much less boilerplate.

---

# 19. Hands-On Exercise

## Goal

Convert one of the raw `curl` LLM calls from Day 1 into Python.

### Step 1 — Create project

Using `uv`:

```bash
uv init day-03-python
cd day-03-python
```

### Step 2 — Install dependencies

```bash
uv add httpx pydantic
```

Or using `venv`:

```bash
python -m venv .venv
```

Activate the environment and run:

```bash
pip install httpx pydantic
```

### Step 3 — Create request model

```python
class LLMRequest(BaseModel):
    model: str
    prompt: str
```

### Step 4 — Create response model

```python
class LLMResponse(BaseModel):
    text: str
```

### Step 5 — Create HTTP function

```python
def generate(request: LLMRequest) -> LLMResponse:
    ...
```

### Step 6 — Send the request with `httpx`

```python
response = httpx.post(...)
```

### Step 7 — Validate the response

```python
result = LLMResponse.model_validate(...)
```

### Step 8 — Print the generated text

```python
print(result.text)
```

---

# 20. Mini Exercise — Build `LLMClient`

Build a small wrapper:

```python
class LLMClient:

    def generate(self, prompt: str) -> str:
        ...
```

A slightly better design:

```python
class LLMClient:

    def __init__(self, api_key: str):
        self.api_key = api_key

    def generate(
        self,
        request: LLMRequest
    ) -> LLMResponse:

        ...
```

Think of this exactly like writing a REST client/service in Java.

```text
Java

LLMService
   ↓
WebClient
   ↓
External API
```

becomes:

```text
Python

LLMClient
   ↓
httpx
   ↓
External API
```

---

# 21. Key Takeaways

The most important concepts from Day 3 are:

```text
venv / uv
    ≈ Maven/Gradle dependency isolation

Type hints
    ≈ Java type declarations

dataclass
    ≈ POJO / Java record

Pydantic BaseModel
    ≈ DTO + validation + serialization

httpx
    ≈ Java HTTP client / WebClient

f-string
    ≈ String interpolation

comprehension
    ≈ concise Stream-style transformation

with
    ≈ try-with-resources
```

The biggest mindset shift is:

> **Python for AI engineering is mostly familiar backend engineering with different syntax and a different ecosystem.**

You already understand the difficult architectural ideas:

```text
DTO
HTTP
JSON
REST
Dependency management
Error handling
Serialization
Configuration
API clients
```

Now you are learning their Python equivalents.

---
