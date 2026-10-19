
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    amount: float = Field(ge=0, description="Amount to calculate")
    percentage: float = Field(ge=0, le=100, description="Percentage from 0 to 100")


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    result: dict
