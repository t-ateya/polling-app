from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
#from app.models.choice import Choice
from .choice import Choice
from fastapi import HTTPException

class PollCreate(BaseModel):
    """The write model"""
    title: str = Field(min_length=5, max_length=50)
    options: List[str]
    expires_at: Optional[datetime] = None 

    @field_validator("options")
    @classmethod
    def validate_options(cls, v: List[str]) -> List[str]:
        if len(v) < 2 or len(v) > 5:
            #raise ValueError("A poll must contain 2 and 5 choices")
            raise HTTPException(
                status_code=400,
                detail= "A poll must contain 2 and 5 choices",
            )
        return v
    
    def create_poll(self) -> "Poll":
        """
            Create a new Poll instance with auto-incrementing labels for Choices, e.g 1, 2, 3
        This will be used in the POST /polls/create endpoint
        """

        # create a list of choices from list[str]
        choices = [
            Choice(description= desc, label=index + 1) 
            for index, desc in enumerate(self.options)
        ]
        #validate expiration date
        if self.expires_at is not None and self.expires_at < datetime.now(timezone.utc):
            #raise ValueError("The expiration date must be in the future")
            raise HTTPException(
                status_code=400,
                detail= "A poll's expiration must be in the future",
            )

        # return a new instance of poll
        return Poll(title=self.title, expires_at=self.expires_at, options=choices)

class Poll(PollCreate):
    """read model"""
    id: UUID = Field(default_factory=uuid4)
    options: List[Choice]
    created_at: Optional[datetime] = Field(
        default_factory= lambda: datetime.now(timezone.utc)
    )

    def is_active(self)->bool:
        if self.expires_at is None:
            return True
        return self.expires_at > datetime.now(timezone.utc)
    
