# Meeting Notes Tailor — PoC (Structured)

## Project Overview

meeting-notes-tailor is a proof-of-concept service designed to transform meeting transcripts into multi-layered, audience-specific summaries using Generative AI. The system recognizes that different stakeholders require distinct insights from the same meeting content:

- **Executives**: High-level strategic summaries highlighting decisions, risks, and leadership requests.

- **Teams**: Clear action items formatted for operational follow-up.
- **New Joiners / Juniors**: Plain-language recaps that explain decisions and context.
- **Optional**: Sentiment analysis per speaker.

This structured approach improves alignment, reduces time spent digesting long meeting notes, and ensures that each stakeholder receives information relevant to their role.

## Tech Stack

- **Language:** Python 3.11
- **Web Framework:** FastAPI
- **Data Validation:** Pydantic
- **Environment Management:** python-dotenv
- **Async Runtime:** asyncio / uvicorn
- **AI Integration:** OpenAI GPT-4o-mini (configurable) / Local Fake LLM
- **Testing:** pytest
- **Containerization:** Docker
- **Build Automation:** Makefile
- **Compute Runtime:** AWS ECS Fargate 
- **Container Registry:** AWS ECR 
- **Networking:** AWS VPC, ALB, Security Groups 
- **Secrets Management:** AWS Secrets Manager 
- **Logging:** AWS CloudWatch Logs 
- **Containerization:** Docker 
- **CI/CD Ready:** Manual Terraform workflow (CLI) 

## Key Features

- AI-powered multi-layered summarization.
- Role-specific prompt templates.
- Supports local offline testing with deterministic outputs (Fake LLM).
- OpenAI GPT-4o-mini integration for dev environment.
- Async FastAPI backend with clear modular structure.
- Docker runtime image for quick deployment.
- Terraform-based AWS infrastructure for deployment.

## Architecture Overview
```
+---------------------------+
|   Client / Frontend       |
|---------------------------|
| - Sends meeting transcripts|
| - Receives role-specific  |
|   summaries               |
+------------+--------------+
             |
             v
+---------------------------+
|   FastAPI Web API          |
|---------------------------|
| - Receives POST /summarize|
| - Validates request using  |
|   Pydantic schemas        |
| - Routes request to       |
|   Summarizer core         |
+------------+--------------+
             |
             v
+---------------------------+
|   Summarizer Core          |
|---------------------------|
| - Parses transcript       |
| - Chunks segments         |
| - Uses role-specific      |
|   prompt templates        |
| - Calls LLM adapter       |
+------------+--------------+
             |
             v
+---------------------------+
|   LLM Adapter Layer        |
|---------------------------|
| - Switches between:       |
|   * Fake LLM (local)     |
|   * OpenAI GPT-4o-mini   |
| - Generates role-based    |
|   summaries asynchronously|
+------------+--------------+
             |
             v
+---------------------------+
|   Output Aggregation       |
|---------------------------|
| - Collates exec summary,  |
|   team actions, and recap  |
| - Optionally includes     |
|   sentiment analysis      |
+------------+--------------+
             |
             v
+---------------------------+
|   Response to Client       |
|---------------------------|
| - Returns JSON with:      |
|   * executive_summary      |
|   * team_actions           |
|   * plain_recap            |
|   * sentiment (optional)   |
+---------------------------+
```

## Project Structure
```
meeting-notes-tailor/
├── app/
│ ├── api/
│ │ └── main.py # FastAPI app and endpoints
│ ├── core/
│ │ ├── summarizer.py # Summarization orchestration
│ │ ├── transcript.py # Transcript parsing and chunking
│ │ ├── prompt_templates.py # Role-specific templates
│ │ └── llm/
│ │ ├── __init__.py # Provider switching logic
│ │ ├── fake.py # Local deterministic LLM
│ │ └── openai.py # OpenAI adapter
│ └── schemas.py # Pydantic schemas for API
├── app/tests/ # Unit tests
├── sample_data/ # Example transcript
|
├── infra/                       # ⬅️ Terraform-based AWS infrastructure
│   ├── provider.tf
│   ├── variables.tf
│   ├── outputs.tf
│   ├── network/
│   │   └── main.tf
│   ├── ecr/
│   │   └── main.tf
│   ├── ecs/
│   │   └── main.tf
│   ├── secrets/
│   │   └── main.tf
│   └── README.md
│
├── Dockerfile # Runtime container
├── Makefile # Local run & build commands
├── requirements.txt # Python dependencies
├── .env.local # Offline LLM mode
├── .env.dev # Dev LLM mode (OpenAI)
└── README.md
```

## Environment Modes

The service can operate in two modes:

| Mode | Env File |	LLM Provider | Description |
|---|---|---|---|
| Local	| .env.local | Fake LLM | Deterministic responses, fully offline for testing logic and development. |
| Dev	| .env.dev | OpenAI GPT-4o-mini	| Connects to OpenAI API for real AI summaries. Requires API key. |

### Example `.env.local`
```
LLM_PROVIDER=fake
FAKE_LLM=true
MODEL_NAME=fake
```

### Example `.env.dev`
```
LLM_PROVIDER=openai
FAKE_LLM=false
OPENAI_API_KEY=your-key-here
MODEL_NAME=gpt-4o-mini
```


## Setup Instructions

### 🧪 Local Setup

1. Unzip project and navigate to root folder.
2. Copy `.env.local` or `.env.dev` to `.env` as appropriate.
3. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.\.venv\Scripts\activate  # Windows
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Run the service:
```bash
uvicorn app.api.main:app --reload
```
6. Open documentation at http://localhost:8000/docs.

### 🐳 Docker Build & Run (Optional)

Build and run the runtime container:
```bash
docker build -t meeting-notes-tailor:local .
docker run -p 8000:8000 meeting-notes-tailor:local
```

## ☁️ AWS Deployment via Terraform (Manual)

1. Build and Push Image to ECR
```bash
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.ap-south-1.amazonaws.com
docker build -t meeting-notes-tailor .
docker tag meeting-notes-tailor:latest <account>.dkr.ecr.ap-south-1.amazonaws.com/meeting-notes-tailor:latest
docker push <account>.dkr.ecr.ap-south-1.amazonaws.com/meeting-notes-tailor:latest
```

2. Deploy Infrastructure

```bash
cd infra
terraform init
terraform plan -var="ecr_image_uri=<account>.dkr.ecr.ap-south-1.amazonaws.com/meeting-notes-tailor:latest"
terraform apply -var="ecr_image_uri=<account>.dkr.ecr.ap-south-1.amazonaws.com/meeting-notes-tailor:latest" -auto-approve
```

After apply:
- Terraform will output the ALB DNS Name.
- Access the API at http://<alb-dns-name>/docs.

### Outputs

| Output             | Description                             |
| ------------------ | --------------------------------------- |
| `alb_dns_name`     | Public endpoint for the FastAPI service |
| `ecr_repo_url`     | ECR repository where image is stored    |
| `ecs_cluster_name` | ECS cluster managing Fargate tasks      |


## API Usage

- **GET /healthz**  — health check

- **POST /summarize** — Transform a transcript into multi-layered summaries.

### Request Example (JSON)

```json
{
  "transcript": "[00:00:05] Alice: Discuss API-first approach...",
  "options": {
    "include_sentiment": true
  }
}
```

### Response Example

```json
{
  "executive_summary": "Strategic decision: adopt API-first approach...",
  "team_actions": [
    {"task": "Define API contract", "owner": "Alice", "due": "2025-10-20", "context": "Discussed API shape"}
  ],
  "plain_recap": "This meeting described the plan to migrate to an API-first architecture...",
  "sentiment": {"Alice": "neutral", "Bob": "neutral"}
}
```

## Core design & flow

1. **Input** — raw transcript text or structured SRT/JSON with speaker labels.
2. **Parse** — transcript.py normalizes and splits transcript into segments (speaker, timestamp, text).
3. **Chunk** — for long meetings, chunks are made for LLM context management.
4. **Prompt** — prompt_templates.py contains role-specific templates.
5. **LLM** — llm_adapter.py sends prompts and returns outputs; supports batching across chunks and simple chain-of-thought-style composition.
6. **Postprocess** — deduplicate, extract action items, sanitize names, timestamp actions to moments in the meeting when possible.

## Prompt templates (examples)

Located in `app/prompt_templates.py`. Keep prompts short and deterministic.

### Executive (short):
```
You are a concise executive assistant. Given the following meeting transcript excerpt, produce a 3-sentence summary emphasizing strategic decisions, risks, and senior-level requests.

Transcript:
"""
{chunk}
"""

Return JSON: {"summary": "..."}
```

### Team actions (bulleted):
```
You are a product ops assistant. From the transcript excerpt, extract concrete action items with: task, owner (if mentioned), due date (if mentioned), and context sentence. Output as JSON list.

Transcript:
{chunk}
```

### Plain recap (for new joiners):
```
You are explaining to a new team member. Provide a short plain-language recap (4-6 sentences) of what happened and why it matters.

Transcript:
{chunk}
```

## LLM Adapter (app/llm_adapter.py)

Provide a thin interface: `generate(prompt, max_tokens=250)` The PoC includes a simple OpenAI-compatible adapter that reads `OPENAI_API_KEY` from env. Swap with any other provider by implementing same function signature.

## Example minimal code snippets

> Note: these are present in the PoC files. This README only shows representative snippets.

- `app/summarizer.py` orchestrates: parse -> chunk -> send prompts -> aggregate
- `app/transcript.py` contains `parse_transcript(text)` that returns `List[Segment]` segments where `Segment = {speaker, start, end, text}`
- `app/prompt_templates.py` exports `TEMPLATES = {"exec": ..., "actions": ..., "recap": ...}`

## Sample transcript

Include `sample_data/sample_transcript.txt` — a 10–15 minute meeting short excerpt with 3 speakers, some decisions, owners, and one or two deadlines so action extraction has content to work on.

## Running Tests

- `test_transcript.py` — validates parsing of speaker labels and timestamps
- `test_summarizer.py` — uses a fake llm_adapter that returns deterministic strings and verifies aggregation into the three outputs.

Run tests with `pytest`.

```bash
pytest app/tests/
```

## Next Steps / Future Enhancements

- Enhanced action item extraction with timestamps.
- Optional sentiment analysis with real NLP models.
- Integration with meeting platforms (Zoom, Teams) for automatic transcript ingestion.
- UI dashboard for viewing summaries by role.
- Async OpenAI SDK or alternative LLM providers.
- Integrate AWS API Gateway for endpoint routing.
- Add async OpenAI SDK integration.
- Introduce CloudFront for caching summaries.
- Use RDS or DynamoDB for transcript storage.
- Enable CI/CD pipeline via GitHub Actions.
