# Day 2 — Math & Transformer Intuition 🧠

# 1. Vectors

## What is a Vector?

For our purposes, a vector is simply:

> **A list of numbers used to represent something.**

Example:

```text
[0.21, -0.43, 0.87, 0.12]
```

In AI systems, vectors are frequently used to represent the **meaning of text**.

Suppose we have:

```text
"I love Java programming"
```

An embedding model might convert it into something conceptually like:

```text
[0.12, -0.31, 0.84, 0.44, ...]
```

Real embedding vectors may contain hundreds or thousands of numbers.

You normally **do not care about the individual numbers**.

You care about the relationship between vectors.

---

## Backend Engineer Mental Model

Think of an embedding as something vaguely similar to a hash:

```text
Text
   ↓
Embedding Model
   ↓
Vector
```

But unlike a normal hash:

```text
SHA256("Java developer")
SHA256("Backend engineer")
```

the outputs don't tell you that the two inputs have related meanings.

Embeddings are different.

```text
Embedding("Java developer")
Embedding("Backend engineer")
```

produce vectors that should be relatively close because their meanings are related.

This property makes embeddings extremely useful for **semantic search**.

---

# 2. Cosine Similarity

Once text has been converted into vectors, we need some way of answering:

> "How similar are these two vectors?"

One common technique is **cosine similarity**.

Don't worry about deriving the formula.

The useful intuition is:

> **Cosine similarity measures how closely two vectors point in the same direction.**

Imagine:

```text
Vector A  ↗

Vector B  ↗
```

They point in approximately the same direction.

Therefore:

```text
High similarity
```

Now imagine:

```text
Vector A  ↗

Vector B  ↘
```

They point in different directions.

Therefore:

```text
Low similarity
```

---

## Why Does This Matter?

Suppose a user searches:

```text
"How do I learn backend development?"
```

Your database contains:

```text
Document 1:
"Java Spring Boot microservices tutorial"

Document 2:
"Best chocolate cake recipe"

Document 3:
"Building REST APIs using Spring Boot"
```

Embedding similarity might conceptually produce:

```text
Document 1 → 0.82
Document 2 → 0.09
Document 3 → 0.87
```

So the system returns:

```text
Document 3
Document 1
```

even though the exact words from the user's query may not appear in those documents.

That is the core idea behind **semantic search**.

This will become extremely important when we study:

```text
Embeddings
      ↓
Vector Database
      ↓
Semantic Search
      ↓
RAG
```

---

# 3. Attention

Attention is one of the most important ideas behind transformers.

A useful mental model is:

> **Each token looks at other relevant tokens and decides how much attention to give them.**

Consider:

```text
The animal didn't cross the street because it was tired.
```

What does:

```text
"it"
```

refer to?

Probably:

```text
"animal"
```

To understand `"it"`, the model needs information from other tokens in the sentence.

Conceptually:

```text
                attention
                    ↓
The animal didn't cross the street because it was tired.
    ↑                                           ↑
    └───────────────────────────────────────────┘
```

The token `"it"` may assign more importance to `"animal"` than `"street"`.

---

# 4. Attention as a Backend Analogy

One useful analogy is a **dynamic weighted JOIN**.

Imagine every token asking:

```text
Which other tokens contain useful information for understanding me?
```

Instead of having a fixed relationship such as:

```sql
orders.customer_id = customers.id
```

the relationships are calculated dynamically.

Conceptually:

```text
Token: "it"

animal  → 0.80
street  → 0.05
cross   → 0.07
tired   → 0.08
```

These numbers are only illustrative.

The important idea is:

> Attention dynamically determines which other tokens matter and by how much.

---

# 5. Self-Attention

When tokens in the same sequence attend to each other, we call it:

```text
Self-Attention
```

Conceptually:

```text
Token 1 ─┬──→ Token 2
         ├──→ Token 3
         └──→ Token 4

Token 2 ─┬──→ Token 1
         ├──→ Token 3
         └──→ Token 4
```

Each token can gather relevant information from other tokens.

This allows the model to build increasingly contextual representations.

---

# 6. Transformer Architecture

Modern LLMs are based on the **Transformer architecture**.

You do NOT need to memorize all of the mathematical details.

At this stage, use this mental model:

```text
Input Text
     ↓
Tokenization
     ↓
Tokens
     ↓
Embeddings
     ↓
┌─────────────────────────┐
│   Transformer Block     │
│                         │
│   Attention             │
│       ↓                 │
│   Feed Forward Network  │
└─────────────────────────┘
     ↓
┌─────────────────────────┐
│   Transformer Block     │
│                         │
│   Attention             │
│       ↓                 │
│   Feed Forward Network  │
└─────────────────────────┘
     ↓
        ...
     ↓
Output Token Probabilities
```

A large language model contains many transformer blocks stacked together.

---

# 7. What Does the Feed-Forward Network Do?

After attention mixes information between tokens, the result passes through a **feed-forward neural network**.

A simplified mental model is:

```text
Attention
    ↓
Gather useful contextual information
    ↓
Feed Forward Network
    ↓
Transform/process that information
```

You don't need to understand the neural-network equations yet.

Remember:

> **Attention mixes information between tokens; the feed-forward network processes the resulting representation.**

---

# 8. From Transformer to Next Token

Recall from Day 1:

LLMs generate text **one token at a time**.

Suppose the input is:

```text
Java is a
```

The model processes the tokens through transformer blocks.

Eventually it produces probabilities such as:

```text
programming → 45%
language    → 35%
coffee      → 10%
framework   → 5%
other       → 5%
```

The decoding strategy then selects a token.

Suppose:

```text
language
```

is selected.

The sequence becomes:

```text
Java is a language
```

The model runs again to predict the next token.

Therefore generation looks conceptually like:

```text
Input
 ↓
Transformer
 ↓
Next-token probabilities
 ↓
Select token
 ↓
Append token
 ↓
Repeat
```

This is **autoregressive generation**.

---

# 9. Gradient Descent

You will frequently hear terms like:

- Gradient
- Gradient descent
- Backpropagation
- Loss function
- Optimizer

As an AI Engineer, you don't initially need the calculus behind them.

Use this mental model:

> **Gradient descent repeatedly nudges model parameters in a direction that reduces prediction error.**

Imagine the model predicts:

```text
Actual answer:   cat
Model predicts:  dog
```

The system calculates how wrong the prediction was.

```text
Prediction
    ↓
Calculate error
    ↓
Adjust model parameters slightly
    ↓
Try again
    ↓
Calculate error
    ↓
Adjust parameters
```

Repeat this process an enormous number of times during training.

Eventually the model becomes better at prediction.

For now:

```text
Gradient Descent
        =
Nudge parameters to reduce error
```

That's enough.

---

# 10. Training vs Inference

This distinction is extremely important.

### Training

```text
Training Data
      ↓
Model makes predictions
      ↓
Calculate error
      ↓
Gradient Descent
      ↓
Update model parameters
      ↓
Repeat
```

The model's parameters change.

### Inference

```text
Prompt
   ↓
Existing trained model
   ↓
Transformer computation
   ↓
Next-token probabilities
   ↓
Generated response
```

The model's base parameters normally **do not change**.

As an AI Engineer, most of your application work happens around:

```text
Inference
```

rather than training a foundation model from scratch.

---

# 11. Putting Everything Together

Our mental model is now:

```text
User Input
    ↓
"Explain Spring Boot"
    ↓
Tokenization
    ↓
Tokens
    ↓
Embeddings
    ↓
Transformer Blocks
    │
    ├── Attention
    │
    └── Feed Forward Network
    ↓
Next-token probabilities
    ↓
Token selected
    ↓
Append token
    ↓
Run again
    ↓
Complete response
```

---
