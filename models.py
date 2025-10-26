from sqlmodel import SQLModel, Field, JSON, Column
from sqlalchemy import Text # <--- Import Text
from typing import Optional, Dict, Any
import datetime

class ReviewResult(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    review_type: str 
    
    scores: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    
    # --- UPDATED ---
    # Changed from max_length=4096 to sa_column=Column(Text) 
    # This allows for much longer feedback strings.
    feedback: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    # --- UPDATED (Proactive Fix) ---
    # Switched from JSON to Text as the error log shows you are saving
    # a string-escaped JSON, not a raw JSON object.
    # This will prevent future "Data too long" errors on this column.
    full_response: Optional[str] = Field(default=None, sa_column=Column(Text))
    
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


# You can remove the Submission model if you aren't using it
class Submission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_name: str
    file_text: str
    embedding: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

