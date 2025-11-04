from fastmcp import FastMCP
import random
import statistics
from datetime import datetime, timezone, timedelta

# 1️⃣ Create the MCP server
mcp = FastMCP(name="Smart Utilities Server")

# 2️⃣ Define tools
@mcp.tool
def roll_dice(num_dice: int = 2, sides: int = 6) -> list[int]:
    """
    Rolls a given number of dice with a specified number of sides.
    Returns a list of results.
    """
    if num_dice <= 0 or sides <= 0:
        raise ValueError("Number of dice and sides must be positive.")
    return [random.randint(1, sides) for _ in range(num_dice)]


@mcp.tool
def summarize_numbers(numbers: list[float]) -> dict:
    """
    Returns basic statistics (count, mean, min, max, stdev) for a list of numbers.
    """
    if not numbers:
        raise ValueError("List of numbers cannot be empty.")
    return {
        "count": len(numbers),
        "mean": statistics.mean(numbers),
        "min": min(numbers),
        "max": max(numbers),
        "stdev": statistics.stdev(numbers) if len(numbers) > 1 else 0.0,
    }


@mcp.tool
def convert_temperature(value: float, unit: str) -> dict:
    """
    Converts temperature between Celsius and Fahrenheit.
    unit = 'C' means convert to Fahrenheit.
    unit = 'F' means convert to Celsius.
    """
    unit = unit.upper()
    if unit == "C":
        result = (value * 9 / 5) + 32
        target = "Fahrenheit"
    elif unit == "F":
        result = (value - 32) * 5 / 9
        target = "Celsius"
    else:
        raise ValueError("Unit must be 'C' or 'F'.")
    return {"input": value, "converted": result, "target_unit": target}

@mcp.tool
def get_current_time(region: str = "UTC") -> str:
    """
    Returns the current time based on the given region.
    For India, use region='India' or 'Indian'.
    Other regions default to UTC.
    """
    # Map region names to UTC offsets (hours)
    timezone_offsets = {
        "india": 5.5,
        "indian": 5.5,
        "utc": 0,
        # You can add more regions here
        "est": -5,
        "pst": -8,
        "cet": 1,
        "gmt": 0
    }

    offset = timezone_offsets.get(region.lower(), 0)

    now_utc = datetime.utcnow().replace(microsecond=0, tzinfo=timezone.utc)
    local_time = now_utc + timedelta(hours=offset)

    # Format timezone string
    sign = '+' if offset >= 0 else '-'
    hours = int(abs(offset))
    minutes = int((abs(offset) - hours) * 60)
    tz_str = f"UTC{sign}{hours:02d}:{minutes:02d}"

    return f"{local_time.strftime('%Y-%m-%d %H:%M:%S')} {tz_str}"


@mcp.tool
def analyze_text(text: str) -> dict:
    """
    Performs basic text analysis — counts words, characters, and sentence estimates.
    """
    if not text.strip():
        raise ValueError("Text cannot be empty.")
    words = text.split()
    sentences = text.count(".") + text.count("!") + text.count("?")
    return {
        "characters": len(text),
        "words": len(words),
        "estimated_sentences": sentences or 1,
    }

# 3️⃣ Run the server
if __name__ == "__main__":
    mcp.run()
