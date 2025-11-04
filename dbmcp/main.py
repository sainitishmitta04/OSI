from fastmcp import FastMCP
from typing import List
from datetime import datetime
import threading

# In-memory mock database with new employee leave data
employee_leaves = {
    "EMP100": {"balance": 15, "history": ["2025-01-10", "2025-02-14"]},
    "EMP101": {"balance": 20, "history": []},
    "EMP102": {"balance": 12, "history": ["2025-03-01"]},
}

# Lock for thread-safe operations
leave_lock = threading.Lock()

# Create MCP server
mcp = FastMCP("LeaveManager")

# Utility: validate date format
def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Tool: Check Leave Balance
@mcp.tool()
def get_leave_balance(employee_id: str) -> dict:
    """Check how many leave days are left for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        return {"employee_id": employee_id, "remaining_balance": data["balance"]}
    return {"error": "Employee ID not found."}

# Tool: Apply for Leave
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> dict:
    """
    Apply leave for specific dates (e.g., ["2025-04-17", "2025-05-01"])
    Validates date format and prevents duplicate leave days.
    """
    if employee_id not in employee_leaves:
        return {"error": "Employee ID not found."}

    # Filter valid and unique dates
    valid_dates = list({d for d in leave_dates if is_valid_date(d)})
    if not valid_dates:
        return {"error": "No valid leave dates provided."}

    with leave_lock:
        available_balance = employee_leaves[employee_id]["balance"]

        if available_balance < len(valid_dates):
            return {
                "error": f"Insufficient leave balance. Requested {len(valid_dates)} day(s), "
                         f"available {available_balance}."
            }

        # Deduct balance and add to history, avoiding duplicates
        for date in valid_dates:
            if date not in employee_leaves[employee_id]["history"]:
                employee_leaves[employee_id]["history"].append(date)
                employee_leaves[employee_id]["balance"] -= 1

    return {
        "employee_id": employee_id,
        "applied_dates": valid_dates,
        "remaining_balance": employee_leaves[employee_id]["balance"]
    }

# Tool: Get Leave History
@mcp.tool()
def get_leave_history(employee_id: str) -> dict:
    """Get leave history for the employee"""
    data = employee_leaves.get(employee_id)
    if data:
        return {
            "employee_id": employee_id,
            "history": sorted(data["history"]) if data["history"] else []
        }
    return {"error": "Employee ID not found."}

# Resource: Greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! How can I assist you with leave management today?"

if __name__ == "__main__":
    mcp.run()
