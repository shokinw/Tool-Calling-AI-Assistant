
from app.schemas import CalculatorInput

data = CalculatorInput(amount=48000, percentage=25)
print(data.model_dump())

try:
    CalculatorInput(amount=48000, percentage=150)
except Exception as error:
    print("Validation error:", error)
