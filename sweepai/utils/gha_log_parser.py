import re


def extract_error_logs(logs: str) -> list[str]:
    error_patterns = [
        r"error[:\s]",
        r"failed[:\s]",
        r"exception[:\s]",
        r"critical[:\s]",
        r"fatal[:\s]"
    ]
    error_logs = []
    for pattern in error_patterns:
        error_logs.extend(re.findall(f".*{pattern}.*", logs, re.IGNORECASE))
    return list(set(error_logs))
