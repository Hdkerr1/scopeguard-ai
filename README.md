# ScopeGuard AI

This repository contains a Streamlit app that generates bulletproof Scope of Work contracts to prevent scope creep. The app uses the OpenAI (or DeepSeek) API to generate contract text and builds a downloadable PDF.

Files added:
- `app.py` - Main Streamlit app (based on the provided script)
- `alternative_app.py` - Alternative/previous version of the app
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container definition for running the Streamlit app
- `vercel.json` - Vercel configuration to deploy the Docker container

## Deploying to Vercel
Vercel supports deploying Docker containers via the `@vercel/docker` builder. Steps:

1. Push this repository to GitHub (already done).
2. In the Vercel dashboard, create a new project and import this GitHub repository.
3. Ensure the `Dockerfile` is used as the build source (Vercel will detect `vercel.json`).
4. In Vercel project settings, add an Environment Variable `OPENAI_API_KEY` (or your DeepSeek key) so the app can call the API.
5. (Optional) Set `PORT` environment variable to `8080` if necessary. Vercel usually provides a port at runtime.

Run locally with Docker:

```bash
docker build -t scopeguard-ai .
docker run -e OPENAI_API_KEY="your_key_here" -p 8080:8080 scopeguard-ai
```

Run locally without Docker:

```bash
python -m pip install -r requirements.txt
export OPENAI_API_KEY="your_key_here"
streamlit run app.py
```

Notes & next steps:
- Replace the placeholder payment link and password flow with a real payment integration (Gumroad, Stripe) and secure password generation/verification.
- Consider deploying to Streamlit Cloud or Render if you prefer a managed Streamlit deployment experience.
