"""HTTP and JSON builtins for DatarScript."""

import json
import urllib.request
import urllib.error
from typing import Any
from .base import BuiltinRegistry
from ..errors import DatarRuntimeError


@BuiltinRegistry.register("http_post")
def http_post(url: str, headers: dict, body: str) -> str:
    """
    Make an HTTP POST request and return the response body.

    Args:
        url: The URL to POST to
        headers: Dictionary of HTTP headers
        body: Request body as a string

    Returns:
        Response body as a string
    """
    try:
        data = body.encode("utf-8")
        req = urllib.request.Request(url, data=data, method="POST")

        # Add headers
        if isinstance(headers, dict):
            for key, value in headers.items():
                req.add_header(str(key), str(value))

        # Make the request
        with urllib.request.urlopen(req, timeout=30) as response:
            return response.read().decode("utf-8")

    except urllib.error.HTTPError as e:
        raise DatarRuntimeError(f"HTTP error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise DatarRuntimeError(f"URL error: {e.reason}")
    except Exception as e:
        raise DatarRuntimeError(f"HTTP POST failed: {str(e)}")


@BuiltinRegistry.register("json_parse")
def json_parse(json_string: str) -> dict:
    """
    Parse a JSON string into a dictionary.

    Args:
        json_string: JSON string to parse

    Returns:
        Parsed data as a dictionary
    """
    try:
        result = json.loads(json_string)
        if isinstance(result, dict):
            return result
        else:
            raise DatarRuntimeError("JSON parse result is not an object")
    except json.JSONDecodeError as e:
        raise DatarRuntimeError(f"JSON parse error: {str(e)}")


@BuiltinRegistry.register("json_get")
def json_get(data: Any, key: Any, default=None) -> Any:
    """
    Get a value from a dictionary or list by key/index.

    Args:
        data: Dictionary or list to get value from
        key: Key or index to look up
        default: Default value if key not found

    Returns:
        The value associated with the key, or default
    """
    if isinstance(data, dict):
        return data.get(str(key), default)
    elif isinstance(data, list):
        try:
            idx = int(key)
            return data[idx]
        except (ValueError, IndexError):
            return default
    else:
        raise DatarRuntimeError("json_get: first argument must be a dictionary or list")


@BuiltinRegistry.register("json_stringify")
def json_stringify(data: dict) -> str:
    """
    Convert a dictionary to a JSON string.

    Args:
        data: Dictionary to convert

    Returns:
        JSON string representation
    """
    try:
        return json.dumps(data)
    except Exception as e:
        raise DatarRuntimeError(f"JSON stringify error: {str(e)}")


@BuiltinRegistry.register("create_headers")
def create_headers() -> dict:
    """
    Create an empty headers dictionary.

    Returns:
        Empty dictionary for HTTP headers
    """
    return {}


@BuiltinRegistry.register("header_set")
def header_set(headers: dict, key: str, value: str) -> dict:
    """
    Set a header value in the headers dictionary.

    Args:
        headers: Headers dictionary
        key: Header name
        value: Header value

    Returns:
        The headers dictionary (for chaining)
    """
    if not isinstance(headers, dict):
        raise DatarRuntimeError("header_set: first argument must be a dictionary")
    headers[str(key)] = str(value)
    return headers
