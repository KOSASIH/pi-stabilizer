"""
Helper functions used throughout the application
"""

import requests
import json
import logging
from typing import List, Dict, Any

def make_request(url: str, method: str = 'GET', data: Dict[str, Any] = None, headers: Dict[str, str] = None) -> requests.Response:
    """
    Make an HTTP request to the given URL
    """
    try:
        response = requests.request(method, url, data=data, headers=headers)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        logging.error(f"Error making request to {url}: {e}")
        return None

def parse_json(response: requests.Response) -> Dict[str, Any]:
    """
    Parse the JSON response from an HTTP request
    """
    try:
        return response.json()
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON response: {e}")
        return {}

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def retry(func: callable, max_retries: int = MAX_RETRIES, timeout: int = DEFAULT_TIMEOUT) -> Any:
    """
    Retry a function with exponential backoff
    """
    retries = 0
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            logging.error(f"Error calling {func.__name__}: {e}")
            retries += 1
            time.sleep(timeout * (2 ** retries))
    raise Exception(f"Failed to call {func.__name__} after {max_retries} retries")
