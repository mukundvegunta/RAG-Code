from typing import List, Tuple, Dict, Any
from pydantic import BaseModel, Field
from typing_extensions import Annotated

class MarketValueSchema(BaseModel):
    """
    Output schema for market value data.
    """
    update_date: str = Field(
        description="Date of the market value record")
    
    market_value: float = Field(
        description="Market value on the given date")
    
    explanation: Dict[str, Any] = Field(
        description="Explanation of how the market value was computed, including factors considered and their weights")
    
    confidence: float = Field(
        description = "Confidence score of the market value estimation, between 0 and 1")
    
    player_id: str = Field(
        description="Unique identifier for the player")
    
