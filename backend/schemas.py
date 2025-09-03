from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Dict, Any, List

# --- Schemas for Intelligence Briefing ---
class NewsArticle(BaseModel):
    title: str
    url: str
    source: str
    sentiment: str
    sentiment_score: float

class SentimentSummary(BaseModel):
    total_items: int
    positive: int
    negative: int
    neutral: int
    error: Optional[str] = None

class IntelligenceBriefing(BaseModel):
    articles: List[NewsArticle]
    sentiment_summary: SentimentSummary

# --- Schema for our LLM Analysis ---
class LLMReport(BaseModel):
    llm_report: str
    error: Optional[str] = None

# --- Main Schema for the 'result' field ---
class JobResult(BaseModel):
    # Data Agent fields
    ticker: Optional[str] = None
    company_name: Optional[str] = None
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    market_cap: Optional[int] = None
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    summary: Optional[str] = None
    website: Optional[str] = None
    
    # Intelligence Agent field
    intelligence_briefing: Optional[IntelligenceBriefing] = None
    
    # LLM Analyst field - THIS IS THE FIX
    llm_analysis: Optional[LLMReport] = None
    
    # General error field
    error: Optional[str] = None

# --- Main Job Schemas for API endpoints ---
class JobCreate(BaseModel):
    ticker: str

class Job(BaseModel):
    id: UUID
    ticker: str
    status: str
    result: Optional[JobResult] = None

    model_config = ConfigDict(from_attributes=True)