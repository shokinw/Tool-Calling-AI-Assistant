
import json
import logging
import ollama

from pydantic import ValidationError
from app.tools import calculate_percentage, get_weather
from app.schemas import CalculatorInput


MODEL = "llama3.1:latest"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# Tools available to the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_percentage",
            "description": "Calculate a percentage of an amount.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "percentage": {"type": "number"}
                },
                "required": ["amount", "percentage"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather and humidity for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }
]


def answer_question(question: str) -> str:
    messages = [{"role": "user", "content": question}]

    # Prevent endless tool-calling loops
    max_steps = 5

    try:
        for step in range(max_steps):
            logger.info("Agent step: %s", step + 1)

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=TOOLS
            )

            # Return the final answer if no tool is requested
            if not response.message.tool_calls:
                logger.info("Final answer generated")

                return (
                    response.message.content
                    or "I couldn't generate an answer."
                )

            # Save the assistant's tool-call message
            messages.append(response.message)

            # Execute requested tools
            for call in response.message.tool_calls:
                name = call.function.name
                arguments = call.function.arguments

                logger.info("Tool selected: %s", name)

                if name == "calculate_percentage":
                    data = CalculatorInput.model_validate(arguments)

                    result = calculate_percentage(
                        amount=data.amount,
                        percentage=data.percentage
                    )

                elif name == "get_weather":
                    city = arguments.get("city")

                    if not isinstance(city, str) or not city.strip():
                        result = {
                            "error": "A valid city name is required."
                        }
                    else:
                        result = get_weather(city.strip())

                else:
                    logger.warning("Unknown tool requested: %s", name)

                    result = {
                        "error": f"Tool '{name}' is not allowed."
                    }

                logger.info("Tool execution completed: %s", name)

                # Send tool result back to the LLM
                messages.append({
                    "role": "tool",
                    "tool_name": name,
                    "content": json.dumps(result)
                })

        logger.warning("Maximum tool-calling steps reached")

        return "Stopped: maximum tool-calling steps reached."

    except (ValidationError, ValueError, TypeError) as error:
        logger.warning("Tool input rejected: %s", error)

        return f"Tool input rejected: {error}"

    except Exception:
        logger.exception("Unexpected assistant error")

        return "Assistant error. Check the terminal logs for details."


if __name__ == "__main__":
    while True:
        question = input("\nYou (type 'exit' to quit): ")

        if question.strip().lower() == "exit":
            break

        print("AI:", answer_question(question))
