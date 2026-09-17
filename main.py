import os

from fastmcp import FastMCP

mcp =FastMCP(name="IT Helpdesk MCP Server")

@mcp.tool
def classify_ticket(issue_description: str) -> dict:
    """
    Classify an IT helpdesk ticket based on its issue description.

    Args:
        issue_description (str): A brief description of the issue reported in the ticket.

    Returns:
        dict: A dictionary containing the classification results for the ticket.
    """
    issue = issue_description.lower()

    if any(word in issue for word in ["vpn", "network", "wifi", "internet"]):
        category = "network"
        team = "Infrastructure Team"

    elif any(word in issue for word in ["password", "login", "authentication"]):
        category = "authentication"
        team = "Identity and Access Management Team"

    elif any(word in issue for word in ["laptop", "keyboard", "mouse", "monitor", "printer", "program"]):
        category = "hardware"
        team = "Desktop Support Team"

    elif any(word in issue for word in ["email", "outlook", "mail", "inbox"]):
        category = "email"
        team = "Messaging Team"

    else:
        category = "general software"
        team = "Application Support Team"

    return {
        "category": category,
        "assigned_team": team
    }


@mcp.tool
def estimate_priority(issue_description: str) -> dict:
    """
    Estimate the priority of an IT helpdesk ticket based on its issue description.

    Args:
        issue_description (str): A brief description of the issue reported in the ticket.

    Returns:
        dict: A dictionary containing the estimated priority for the ticket.
    """
    issue = issue_description.lower()

    if any(word in issue for word in ["urgent", "immediately", "asap", "critical", "outage"]):
        priority = "Critical"
        sla = "1-hour"

    elif any(word in issue for word in ["unable", "blocked", "cannot", "failed"]):
        priority = "High"
        sla = "4-hour"
    
    elif any(word in issue for word in ["slow", "error", "issue"]):
        priority = "Medium"
        sla = "8-hour"
    else:
        priority = "low"
        sla = "2 Business Days"

    return {
        "priority": priority,
        "sla": sla
    }

@mcp.tool
def generate_troubleshooting_steps(issue_type: str) -> list[str]:
    """
    Generate troubleshooting steps for common issues.

    Args:
        issue_type (str): The type of issue (e.g., "vpn", "authentication", "hardware", "email", "general software").

    Returns:
        list[str]: A list of troubleshooting steps for the specified issue type.
    """
    issue = issue_type.lower()

    if issue == "vpn":
        return [
            "Check if the network cables are properly connected.",
            "Restart the router or switch.",
            "Verify the VPN connection settings.",
            "Check for any network outages in your area."
        ]
    elif issue == "password":
        steps = [
            "Ensure you are using the correct username and password.",
            "Reset your password if necessary.",
            "Check if your account is locked or disabled.",
            "Verify multi-factor authentication settings."
        ]
    elif issue == "hardware":
        steps = [
            "Check if the hardware is properly connected.",
            "Restart the device.",
            "Run hardware diagnostics.",
            "Replace faulty hardware components if needed."
        ]
    elif issue == "email":
        steps = [
            "Check your email account settings.",
            "Ensure you have an active internet connection.",
            "Clear the email client cache.",
            "Verify the email server status."
        ]
    else:  # general software (default case)
        steps = [
            "Restart the application.",
            "Check for software updates.",
            "Reinstall the application if necessary.",
            "Consult the application support documentation."
        ]

    return steps

@mcp.tool
def estimate_resolution_time(priority: str) -> dict:
    """
    Estimate the resolution time for an IT helpdesk ticket based on its priority.

    Args:
        priority (str): The priority level of the ticket (e.g., "Critical", "High", "Medium", "Low").

    Returns:
        dict: A dictionary containing the estimated resolution time for the ticket.
    """
    priority = priority.lower()

    mapping={
        "critical": "2 hours",
        "high": "8 hours",
        "medium": "1 business day",
        "low": "3 business days"
    }

    resolution_time = mapping.get(priority, "to be determined")

    return {
        "resolution_time": resolution_time
    }


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    mcp.run(transport="http", host="0.0.0.0", port=port)
