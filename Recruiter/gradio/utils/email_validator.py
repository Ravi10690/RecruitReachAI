"""Email validation utilities."""

import re

# Email validation regex pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

def is_valid_email(email: str) -> bool:
    """
    Check if an email address is valid.
    
    Args:
        email: Email address to check.
        
    Returns:
        True if the email is valid, False otherwise.
    """
    return bool(re.match(EMAIL_PATTERN, email))
