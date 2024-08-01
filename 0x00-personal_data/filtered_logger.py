#!/usr/bin/env python3
"""
Filter datum module
"""
import logging
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """
    Parameters
    ----------
    fields(List[str]): a list of strings representing all fields to obfuscate
    redaction(str): a string representing by what the field will be obfuscated
    message(str): a string representing the log line
    separator(str): a string representing by which character is separating all
    fields in the log line (message)
    """
    pattern = f"({'|'.join(fields)})=[^{separator}]*"
    return re.sub(pattern, lambda m: f"{m.group(1)}={redaction}", message)
