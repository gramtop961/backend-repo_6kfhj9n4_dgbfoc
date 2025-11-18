"""
Database Schemas for Tarot Blog

Each Pydantic model represents a collection in MongoDB. The collection name is the lowercase of the class name.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import date

class Horoscope(BaseModel):
    """Horoscopes collection schema
    Collection: "horoscope"
    """
    sign: Literal[
        "aries","taurus","gemini","cancer","leo","virgo",
        "libra","scorpio","sagittarius","capricorn","aquarius","pisces"
    ] = Field(..., description="Zodiac sign")
    period: Literal["daily", "weekly", "monthly"] = Field(..., description="Horoscope period type")
    title: str = Field(..., description="Short title or headline")
    content: str = Field(..., description="Horoscope text content")
    date_from: Optional[date] = Field(None, description="Start date for this horoscope period")
    date_to: Optional[date] = Field(None, description="End date for this horoscope period")

class Paidreading(BaseModel):
    """Paid reading requests
    Collection: "paidreading"
    """
    name: str = Field(..., description="Client name")
    email: str = Field(..., description="Client email for delivery")
    question: str = Field(..., description="Client question or focus area")
    package: Literal["mini", "standard", "deep"] = Field(..., description="Selected package tier")
    status: Literal["pending", "in_progress", "completed"] = Field("pending", description="Fulfillment status")

class Readingsession(BaseModel):
    """Pick-a-card sessions
    Collection: "readingsession"
    """
    prompt: Optional[str] = Field(None, description="User intention or prompt")
    picked_cards: List[str] = Field(..., description="List of card names picked")
    notes: Optional[str] = Field(None, description="Optional interpretation notes")

# Example schemas kept for reference (not used directly by app)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
