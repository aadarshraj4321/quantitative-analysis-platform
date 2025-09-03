# Quantitative Analysis Platform
> A multi-agent AI system designed to provide retail investors with hedge-fund-level research and insights


## The Problem
Retail investors are at a massive disadvantage. They lack the sophisticated tools, real-time data aggregation, and unbiased analysis that hedge funds use daily. Decisions are often driven by emotion and noise from social media, leading to poor outcomes. This platform was built to bridge that gap.

## Features
- **Multi-Agent Pipeline:** A robust, asynchronous backend where specialized AI agents collaborate to build a complete analysis.
- **Data Agent:** Fetches real-time, comprehensive financial data for any stock.
- **Intelligence Agent:** Scrapes Google News, Yahoo Finance, and Reddit to gather and analyze market sentiment.
- **LLM Analyst Agent:** Utilizes **Google's Gemini 1.5 Flash** to analyze all collected data, identify trends, and generate a human-like investment thesis with a forecast and actionable strategy.
- **Interactive Dashboard:** A clean, modern React frontend to visualize the data, including news feeds and historical price charts.
- **Job History:** Users can view and revisit all their past analyses.


## Tech Stack & Architecture

### Frontend
- **React (Vite):** For a fast and modern user interface.
- **Tailwind CSS:** For professional and responsive styling.
- **Recharts:** For beautiful and interactive data visualizations.
- **Axios:** For seamless communication with the backend API.

### Backend
- **FastAPI:** A high-performance Python framework for building the API.
- **Celery & Redis:** To manage the asynchronous, multi-step agent pipeline, ensuring the UI is always fast and responsive.
- **PostgreSQL (Neon):** A scalable, serverless cloud database for storing job data.
- **SQLAlchemy & Alembic:** For robust database interaction and schema migrations.
- **LangChain & Google Gemini 1.5 Flash:** The core AI engine for the Analyst Agent.


### Architecture
```mermaid
graph TD
    A[User on React Frontend] -->|1. POST /jobs (ticker)| B(FastAPI Backend);
    B -->|2. Dispatch Task| C[Redis Queue];
    C -->|3. Pick up Job| D(Celery Worker);
    D -->|4. Run Pipeline| E[Agent 1: Data];
    E -->|5. Update DB| F[(Neon DB)];
    D -->|6. Run Pipeline| G[Agent 2: Intelligence];
    G -->|7. Update DB| F;
    D -->|8. Run Pipeline| H[Agent 3: LLM Analyst];
    H -->|9. Call Gemini API| I{Gemini 1.5 Flash};
    I -->|10. Return Thesis| H;
    H -->|11. Final Update| F;
    A -->|12. GET /jobs/{id} (Polling)| B;
    B -->|13. Read Status/Result| F;
end

## Local Setup

