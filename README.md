⚖️ LEXI — Evidence-Grounded Judicial Simulation

LEXI is a human-in-the-loop, AI-assisted judicial decision-support system that models constitutional screening, adversarial legal workflows, and explainable verdict reasoning under the Indian judicial framework.

LEXI is not a legal chatbot and does not adjudicate cases.
Instead, it enforces legally defined procedural gates and standards of proof, ensuring that humans remain responsible for judgment.



1️⃣ Overview

LEXI is designed to mirror real-world judicial reasoning rather than replace it.

Key characteristics:

Treats incidents as allegations, not conclusions

Enforces mandatory constitutional screening before case registration

Supports adversarial submissions from both parties

Uses AI only for retrieval and constrained fact extraction

Applies deterministic legal thresholds for verdict logic

Produces fully explainable verdicts

The system prioritizes legal discipline, transparency, and human accountability.



2️⃣ End-to-End Workflow
1. Incident Entry

A petitioner submits an incident description

The incident is treated strictly as an allegation

No assumptions of illegality are made


2. Constitutional Screening (Mandatory Gate)

The incident is embedded and matched against the Indian Constitution

Relevant Articles are retrieved from the constitution_articles table using pgvector

An LLM explains relevance only (no legal judgment)

Outcome:

If no constitutional issue is detected → case registration is blocked

If a constitutional violation is detected → user may proceed


3. Case Registration

A unique Case ID is generated

The incident becomes the ground-truth 
context for the entire case

All future reasoning is anchored to this incident


4. Adversarial Workflow

LEXI-A (Petitioner) submits claims and supporting evidence

LEXI-B (Respondent) submits rebuttals and counter-evidence

This models real adversarial court proceedings


5. Evidence Processing

Supported formats:

PDF

Text files

Images (OCR enabled)

Evidence processing steps:

Text extraction (OCR where required)

Cryptographic hashing for integrity

Semantic embedding for retrieval


6. Incident-Anchored Fact Extraction

AI extracts only facts directly related to the registered incident

Constraints enforced:

No external knowledge

No speculative inference

If irrelevant → output is “NO RELEVANT FACTS”

This prevents hallucination and scope drift


7. Human Assessment of Proof

A human evaluator assigns a degree of proof (0–1) against the respondent

This represents confidence, not probability

The system does not score or override this input


8. Deterministic Verdict Logic

Based on case type, fixed legal thresholds are applied:

Criminal cases: Beyond reasonable doubt

Civil cases: Preponderance of evidence


Rule:

If human score ≥ legal threshold → Guilty
Else → Not Guilty


No AI judgment is involved.


9. Explainable Verdict Output

The final verdict includes:

Verdict (Guilty / Not Guilty)

Case type and legal standard

Threshold applied

Degree of proof provided

Number of incident-relevant facts considered

Clear explanation of why the threshold was or wasn’t met



3️⃣ Core Design Principles

Human-in-the-loop by design

No AI adjudication

Deterministic legal logic

Explainable outcomes

Domain-grounded AI usage

Procedural discipline over automation

“AI assists with understanding and organizing information, but humans remain responsible for judgment.”



4️⃣ Evaluation Summary

The system was evaluated on retrieval quality, relevance, determinism, and human alignment, not classification accuracy.

Constitutional article retrieval recall@3: ~90%

Evidence-to-fact extraction precision: ~80–85%

Verdict decision consistency: 100%

Human–system verdict agreement: >90%



5️⃣ Tech Stack

Backend: FastAPI

Database: PostgreSQL (Supabase + pgvector)

Embeddings: Jina Embeddings

LLM Assistance: Gemini API (constitutional analysis & fact extraction)

Frontend: Streamlit




⚠️ Disclaimer

LEXI is an educational and research-oriented judicial simulation system.

It does not:

Provide legal advice

Replace lawyers or judges

Issue real judicial decisions
