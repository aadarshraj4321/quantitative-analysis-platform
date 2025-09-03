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


Local Setup & Installation
Follow these steps to run the project locally.
Prerequisites:
Docker & Docker Compose
Python 3.10+
Node.js & npm


1. Clone the repository:
code
Bash
git clone https://github.com/your-username/quantitative-analysis-platform.git
cd quantitative-analysis-platform


2. Set up environment variables:
Create a .env file in the root of the project by copying the example:
code
Bash
cp .env.example .env


3. Build and run the services:
code
Bash
docker-compose up --build -d


4. Access the applications:
Frontend: http://localhost:5173
Backend API Docs: http://localhost:8000/docs
💡 Key Challenges & Learnings
Asynchronous Workflow: Building a resilient, multi-stage pipeline with Celery required careful state management and error handling to ensure the process could continue even if one of the scraping agents failed.
Database Session Management: The most challenging bug was ensuring that the SQLAlchemy database sessions were correctly handled within the forked processes of the Celery workers. The final solution involved a "one task, multiple commits" pattern for maximum reliability.
AI Prompt Engineering: Crafting the perfect prompt for the Gemini Analyst Agent was an iterative process. It involved structuring the input data and giving the LLM a clear "persona" and a required output format (Markdown) to get consistent, high-quality results.


Fill in the Blanks:
Take a great screenshot of your final, beautiful dashboard and save it in your project. Update the path in the README.md.
Create a .env.example file in your root directory. Copy your .env file, but remove your actual secret keys and replace them with placeholders like your_key_here. This is a professional standard.
