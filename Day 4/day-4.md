# Day 4 — Python for AI Engineers, Part 2: Async + FastAPI

## 1. Async Python through a Java backend lens

| Python                           | Approximate Java connection                                     | Key distinction                                                                                                                                   |
| -------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `async def`                      | A method participating in an asynchronous pipeline              | Calling it produces a coroutine; it does not run the body to completion immediately.                                                              |
| `await operation()`              | Waiting for a `CompletableFuture` result in a composed pipeline | At a genuine async I/O wait, the current coroutine suspends and the event loop can run other work. It is **not** like blocking on `future.get()`. |
| `asyncio.gather(a(), b())`       | Combining independent futures                                   | The operations can overlap while waiting; this alone does not make CPU work parallel.                                                             |
| `async with httpx.AsyncClient()` | Manage an HTTP client resource                                  | Client calls such as `await client.post(...)` can yield during network I/O.                                                                       |
| Event loop                       | Scheduler for many in-flight I/O operations                     | A long synchronous operation inside a coroutine can stall other coroutines on that loop.                                                          |

An LLM API call spends much of its wall time waiting for a remote server. An asynchronous HTTP client lets the server handle other ready requests during that wait. **Async improves concurrency under I/O load; it does not make one model reply inherently faster.** For CPU-heavy local inference, use appropriate worker/process infrastructure rather than expecting `async` to speed up computation. FastAPI's async guidance distinguishes async I/O from ordinary blocking libraries. [FastAPI concurrency guide](https://fastapi.tiangolo.com/async/)

### Try it: sequential versus concurrent waits

Save as `async_demo.py`:

```python
import asyncio
import time


async def simulated_llm(name: str) -> str:
    await asyncio.sleep(1)  # Yields control; stands in for network waiting.
    return f"Reply for {name}"


async def main() -> None:
    start = time.perf_counter()
    first = await simulated_llm("A")
    second = await simulated_llm("B")
    print("sequential:", first, second, f"{time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    first, second = await asyncio.gather(
        simulated_llm("A"), simulated_llm("B")
    )
    print("concurrent:", first, second, f"{time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
```

Run `python async_demo.py`. Expect roughly two seconds sequentially and one second concurrently; actual times vary. `asyncio.sleep()` deliberately suspends its task. `gather()` schedules the awaitables together and returns results in input order. [Python asyncio tasks](https://docs.python.org/3/library/asyncio-task.html)

> **Common mistake:** `time.sleep(2)` inside `async def` blocks the event-loop thread. `await asyncio.sleep(2)` yields. Likewise, `requests.post(...)` or `httpx.post(...)` is synchronous; use an async client and `await` in an async route. Do not use `asyncio.run()` inside a FastAPI route; FastAPI already runs it in an event-loop context.

## 2. FastAPI as a small Spring Boot service

| Spring Boot                                | FastAPI                                                        |
| ------------------------------------------ | -------------------------------------------------------------- |
| `@RestController` + `@PostMapping("/ask")` | `app = FastAPI()` + `@app.post("/ask")`                        |
| `@RequestBody AskRequest`                  | Route parameter `request: AskRequest`                          |
| DTO with `@Valid` and field constraints    | Pydantic `BaseModel` with `Field(...)` constraints             |
| Response DTO                               | `response_model=AskResponse`                                   |
| OpenAPI/Swagger setup                      | Generated schema at `/openapi.json`; interactive UI at `/docs` |

The mapping is conceptual: FastAPI's request parsing, validation, and response modeling have their own behavior. A malformed request produces a **422** validation response by default. Request types and response models also contribute to generated OpenAPI documentation. [Request body](https://fastapi.tiangolo.com/tutorial/body/) · [Response model](https://fastapi.tiangolo.com/tutorial/response-model/) · [First steps](https://fastapi.tiangolo.com/tutorial/first-steps/)

## 3. Hands-on: build a non-blocking `/ask` endpoint

Create a new directory or continue your Day 3 environment. Choose **one** setup path:

```bash
# If using uv in an existing project:
uv add "fastapi[standard]" httpx

# Or if using a previously activated venv:
python -m pip install "fastapi[standard]" httpx
```

FastAPI's standard install includes its development server command. [Installation tutorial](https://fastapi.tiangolo.com/tutorial/)

Save this as `main.py`:

```python
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Day 4 LLM Service")


class AskRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=500)


class AskResponse(BaseModel):
    answer: str
    model: str


async def generate_answer(prompt: str) -> str:
    # Replace this simulated network wait with an async LLM client later.
    await asyncio.sleep(1)
    return f"Demo response to: {prompt}"


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest) -> AskResponse:
    answer = await generate_answer(request.prompt)
    return AskResponse(answer=answer, model="simulated-llm")
```

Start it in one terminal:

```bash
# uv project:
uv run fastapi dev main.py

# Activated venv:
fastapi dev main.py
```

Try these in another terminal. In PowerShell, use `curl.exe` rather than the `curl` alias:

```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"prompt":"Explain embeddings in one sentence"}'

curl -X POST http://127.0.0.1:8000/ask \
  -H 'Content-Type: application/json' \
  -d '{"prompt":""}'
```

The first call should return an `answer` and `model` after about one second. The second should return HTTP **422** with a field validation error. Open `http://127.0.0.1:8000/docs`, try the same request there, and inspect `http://127.0.0.1:8000/openapi.json`. The `/health` endpoint should return `{"status":"ok"}`.

**Windows PowerShell equivalent:**

```powershell
curl.exe -X POST "http://127.0.0.1:8000/ask" -H "Content-Type: application/json" -d '{"prompt":"Explain embeddings"}'
```

### Observe concurrency

Send two valid `/ask` calls at about the same time from two terminals. Each includes a one-second simulated wait, but their waits can overlap on an async server. Terminal scheduling and other overhead affect the exact timing. This demonstration shows overlapping I/O waits, not parallel model computation.

## 4. Replace the simulation with an outbound async call

In Day 3 you used a typed Python HTTP client. The essential async change is using `httpx.AsyncClient` and awaiting the request:

```python
import httpx


async def fetch_json(url: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
```

Adapt the **real provider URL, headers, request JSON, and Pydantic response model from your Day 3 exercise**. For an LLM API, keep credentials in environment variables and follow the provider's current request schema. Do not substitute `httpx.post(...)` inside `async def`. When an application makes many outbound calls, reuse a client with an appropriate application lifecycle instead of creating a new client in a hot loop; this example keeps resource handling easy to see. Set an explicit timeout and handle upstream failures before using it in production. [HTTPX async support](https://www.python-httpx.org/async/) · [HTTPX timeouts](https://www.python-httpx.org/advanced/timeouts/)

**Extension:** Add an endpoint that accepts two prompts and uses `asyncio.gather` to call `generate_answer` for each. Explain why two simulated one-second waits should take roughly one second in total. For a real provider, limit concurrency and account for its rate limits.
