---
title: Quantitative Analysis Platform
emoji: 📈
colorFrom: green
colorTo: emerald
sdk: docker
pinned: false
---

# Quantitative Analysis Platform
> A multi-agent AI system designed to provide retail investors with hedge-fund-level research and insights


## The Problem
Retail investors face a massive information asymmetry compared to institutional hedge funds. They lack access to:
*   Real-time aggregation of financial news and social media sentiment.
*   Sophisticated tools to interpret raw financial data.
*   Unbiased, data-driven analysis to counter emotional decision-making.

This platform was built to bridge that gap, providing a suite of AI-powered tools that mimic a team of hedge fund analysts, accessible to anyone for free.


## Features
*   **Multi-Agent Pipeline:** A robust, asynchronous backend where specialized AI agents collaborate in a three-stage pipeline to build a complete analysis.
*   **Data Agent:** Fetches real-time, comprehensive financial data, including key metrics, daily price action, and company officer information for any stock.
*   **Intelligence Agent:** Scans the web in real-time, scraping Google News, Yahoo Finance, and Reddit to gather and analyze market sentiment using a finance-tuned NLP model.
*   **LLM Analyst Agent:** The "brain" of the operation. It utilizes **Google's Gemini 1.5 Flash** to synthesize all the collected quantitative and qualitative data. It analyzes the last 100 days of price action and the latest news to generate a human-like investment thesis, complete with a 30-day forecast, bull/bear cases, and an actionable strategy.
*   **Interactive Dashboard:** A clean, modern React frontend to visualize the analysis. It provides a real-time status of the agent pipeline and displays the final report in a beautiful, easy-to-read format.
*   **Job History:** Users can view and revisit all their past analyses, making the platform a persistent research tool.



## Tech Stack & Architecture
This project is built with a modern, scalable, and containerized architecture.

### **Frontend**
*   **React (Vite):** For a high-performance, modern user interface.
*   **Tailwind CSS:** For professional, utility-first styling and a responsive design.
*   **Recharts:** For creating beautiful and interactive data visualizations.
*   **Axios:** For seamless and robust communication with the backend API.

### **Backend**
*   **FastAPI:** A high-performance Python framework for building the core API.
*   **Celery & Redis:** Manages the asynchronous, multi-agent pipeline. This ensures the UI is always fast and responsive, while the heavy lifting is done in the background.
*   **PostgreSQL (Neon):** A scalable, serverless cloud database for storing all job data and results.
*   **SQLAlchemy & Alembic:** The industry standard for robust database interaction and schema migrations.
*   **LangChain & Google Gemini 1.5 Flash:** The core AI engine for the Analyst Agent, enabling sophisticated reasoning and report generation.

### **How the Architecture Works**

The system is designed as a decoupled, multi-service application orchestrated by Docker Compose.
graph TD
    "User's Browser"
        A[React Frontend]
    

    "Backend Services (Docker)"
        B(FastAPI Backend API)
        C[Redis Queue]
        D(Celery Worker)
   
    
    "External Services"
        E[(Neon DB)]
        F{Data Sources<br/>(yfinance, Google, Reddit)}
        G{Google AI<br/>(Gemini 1.5 Flash)}
    

    A -->|1. POST /jobs (ticker)| B;
    B -->|2. Creates Job Record| E;
    B -->|3. Dispatches Task| C;
    
    C -->|4. Worker Picks Up Task| D;
    
    D -->|5. Agent 1: Data| F;
    D -->|6. Updates DB| E;

    D -->|7. Agent 2: Intelligence| F;
    D -->|8. Updates DB| E;

    D -->|9. Agent 3: Analyst| G;
    D -->|10. Final Update| E;

    A -->|11. GET /jobs/{id} (Polling)| B;
    B -->|12. Reads Job Status/Result| E;


- The user enters a ticker on the React Frontend.
- A request is sent to the FastAPI Backend, which creates a job record in the Neon Database.
- FastAPI dispatches the main analysis task to the Redis Queue.
- The Celery Worker picks up the task and begins the three-stage pipeline.
- It calls the Data Agent tools to fetch data from yfinance.
- It then calls the Intelligence Agent tools to scrape Google News & Reddit.
- Finally, it calls the Analyst Agent, which sends all the collected data in a detailed prompt to the Gemini 1.5 Flash API.
- The worker saves the final, complete report to the database.
- Meanwhile, the React frontend polls the API every few seconds, updating the UI with the live status of the pipeline until the final result is ready to be displayed.


## Local Setup & Installation
- Follow these steps to run the project locally.
 - Prerequisites:
    - Docker & Docker Compose: The easiest way to run the entire stack.
    - Python 3.10+
    - Git: For cloning the repository.
    - Node.js & npm
    - A Hugging Face Account: (Needed if you want to re-download the sentiment model).


1. Clone the repository:
```bash
git clone https://github.com/your-username/quantitative-analysis-platform.git
cd quantitative-analysis-platform
```


2. Set up environment variables:
- The project requires a .env file with your secret keys. Create one by copying the example file:
```bash
Create a .env file in the root of the project by copying the example:
cp .env.example .env
```

- Now, open the .env file and add your own API keys:
    - DATABASE_URL: Your connection string from your Neon PostgreSQL project.
    - GOOGLE_API_KEY: Your API key for the Gemini model from Google AI Studio.


3. The Sentiment Model:
The sentiment analysis model (ProsusAI/finbert) is included in the ml_models directory to ensure the application works offline and avoids runtime download issues. If you need to re-download it, follow the instructions in the Hugging Face documentation.

4. Build and Run with Docker Compose:
This single command will build the Docker images for all services and start the entire platform.
code
```bash
docker-compose up --build -d
```

4. Access the applications:
```bash
Frontend: http://localhost:5173
Backend API Docs: http://localhost:8000/docs
```

## Key Challenges & Learnings
 - Asynchronous Workflow: Building a resilient, multi-stage pipeline with Celery required careful state management and error handling to ensure the process could continue even if one of the scraping agents failed.
 - Database Session Management: The most challenging bug was ensuring that the SQLAlchemy database sessions were correctly handled within the forked processes of the Celery workers. The final solution involved a "one task, multiple commits" pattern for maximum reliability.
 - AI Prompt Engineering: Crafting the perfect prompt for the Gemini Analyst Agent was an iterative process. It involved structuring the input data and giving the LLM a clear "persona" and a required output format (Markdown) to get consistent, high-quality results.

