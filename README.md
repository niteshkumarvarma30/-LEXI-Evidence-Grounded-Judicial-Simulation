LEXI — Evidence-Grounded Judicial Simulation

A human-in-the-loop, AI-assisted judicial decision-support system modeling constitutional screening, adversarial legal workflows, and explainable verdict reasoning.

1) Overview:-

LEXI is an evidence-grounded judicial simulation system designed to reflect real-world legal workflows under the Indian judicial framework.
The system assists in constitutional screening, evidence processing, and legal reasoning, while ensuring that humans retain authority over final judgments.

Unlike chatbot-style legal tools, LEXI does not adjudicate cases.
Instead, it enforces legally defined standards of proof and provides transparent, explainable verdict reasoning.




2) End-to-End Workflow:-

1)Incident Entry

-> A petitioner describes an alleged incident.

-> The incident is treated as an allegation, not a conclusion.


2) Constitutional Screening (Mandatory Gate)

-> Semantic retrieval identifies relevant Articles of the Indian Constitution.

-> Case registration is blocked if no constitutional issue is detected.


3) Case Registration

-> A unique Case ID is generated.

-> The incident becomes the ground-truth context for all further reasoning.


4) Adversarial Workflow

-> LEXI-A (Petitioner) submits claims and evidence.

-> LEXI-B (Respondent) submits rebuttals and counter-evidence.


5) Evidence Processing

-> Supports PDF, text, and image uploads.

-> OCR and text extraction are applied as needed.

-> Evidence integrity is preserved via hashing.


6) Incident-Anchored Fact Extraction

-> AI extracts only facts directly relevant to the incident.

-> Irrelevant or hallucinated content is rejected.


7) Human Assessment of Proof

-> A human evaluator assigns a degree of proof (0–1) against the respondent.


8) Deterministic Verdict Logic

-> Fixed legal thresholds are applied:

-> Criminal: beyond reasonable doubt

-> Civil: preponderance of evidence


9) Explainable Verdict Output

-> Verdict with structured legal reasoning is generated.






3) Design Principles

-> Human-in-the-loop by design

-> No AI adjudication

-> Deterministic legal logic

-> Explainable outcomes

-> Domain-grounded AI usage



4) Evaluation Summary

-> Constitutional article retrieval recall@3: ~90%

-> Evidence-to-fact extraction precision: ~80–85%

-> Verdict decision consistency: 100%

-> Human–system verdict agreement: >90%

-> Evaluation focuses on retrieval quality, relevance, determinism, and human alignment, not classification accuracy.



5) Tech Stack

-> Backend: FastAPI

-> Database: PostgreSQL (Supabase + pgvector)

-> Embeddings: Jina Embeddings

-> LLM Assistance: Ollama (mistral:7b-instruct)

-> Frontend: Streamlit



⚠️ Disclaimer

This system is for educational and research purposes only.
It does not provide legal advice or real judicial decisions.
