# from sqlalchemy import Column, String, JSON
# from sqlalchemy.dialects.postgresql import UUID
# import uuid
# from core.database import Base

# class AnalysisJob(Base):
#     __tablename__ = "analysis_jobs"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     ticker = Column(String, nullable=False, index=True)
#     status = Column(String, default="PENDING", nullable=False)
#     result = Column(JSON, nullable=True)



from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from core.database import Base
from datetime import datetime

class AnalysisJob(Base):
    __tablename__ = "analysis_jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ticker = Column(String, nullable=False, index=True)
    status = Column(String, default="PENDING", nullable=False)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False) 