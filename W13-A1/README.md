# Week 13 Activity 1: LLM-Powered CV Feedback and Optimization

This project is a backend application that generates constructive, personalized CV feedback and produces an optimized CV version for a target role. It is designed for the MSE803 Data Analytics Week 13 Activity 1 submission.

## Features

- Analyze CV text or uploaded CV files.
- Generate feedback on content, structure, presentation, and ATS keywords.
- Optimize a CV for a Software Engineer target role.
- Export the optimized CV as a `.docx` document.
- Use Gemini API when an API key is configured.
- Fall back to a local demo feedback engine when no API key is available.

## Technology Stack

- Python
- FastAPI
- Gemini API through the REST Interactions API
- python-docx for `.docx` export
- pypdf and python-docx for file text extraction

## Gemini API Key

Create a free Gemini API key from Google AI Studio:

https://aistudio.google.com/app/apikey

Google's Gemini Developer API provides a free tier for small projects. Free-tier prompts and outputs may be used by Google to improve products, so do not upload sensitive personal CV information unless you are comfortable with that policy.

## Setup

```bash
cd /Users/ginoted/Documents/GitHub/MSE803DataAnalytics/W13-A1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Optional: open `.env` and add your key.

```bash
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash
```

If `GEMINI_API_KEY` is empty, the application runs in demo mode.

## Run the API

```bash
uvicorn app.main:app --reload
```

Open the interactive API docs:

```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Health Check

```http
GET /health
```

### Analyze CV Text

```http
POST /api/cv/analyze
Content-Type: application/json
```

```json
{
  "target_role": "Software Engineer",
  "cv_text": "Paste CV text here..."
}
```

### Analyze Uploaded CV

```http
POST /api/cv/analyze-file
```

Form fields:

- `file`: `.txt`, `.md`, `.docx`, or `.pdf`
- `target_role`: for example, `Software Engineer`

### Optimize CV Text

```http
POST /api/cv/optimize
Content-Type: application/json
```

```json
{
  "target_role": "Software Engineer",
  "cv_text": "Paste CV text here..."
}
```

### Download Optimized DOCX

```http
POST /api/cv/optimize-docx
Content-Type: application/json
```

This returns `optimized_cv.docx`.

## Generate the Sample Submission CV

This command works without a Gemini API key:

```bash
python scripts/generate_sample_cv.py
```

Generated files:

- `output/sample_feedback.json`
- `output/optimized_cv_sample.md`
- `output/optimized_cv_sample.docx`

To generate the final submission CV using the configured provider, run:

```bash
python scripts/generate_submission_cv.py
```

With `GEMINI_API_KEY` set, this creates Gemini-powered files such as:

- `output/submission_feedback_gemini.json`
- `output/optimized_cv_gemini.md`
- `output/optimized_cv_gemini.docx`

## Test

The included tests use Python's built-in unittest module:

```bash
python -m unittest discover -s tests
```

## Project Structure

```text
W13-A1/
  app/
    main.py
    config.py
    schemas.py
    services/
      cv_feedback.py
      cv_parser.py
      cv_document.py
      gemini_client.py
      rule_based_cv.py
  examples/
    sample_cv.txt
  scripts/
    generate_sample_cv.py
  tests/
    test_rule_based_cv.py
  output/
  requirements.txt
  .env.example
  README.md
```

## Submission Notes

Submit:

1. The GitHub repository containing this project.
2. The optimized CV file: `output/optimized_cv_sample.docx`.
3. The repository link in the assignment submission portal.
