"""HTTP and JSON builtins."""

import urllib.request
import urllib.error
import json
from typing import Any
from .base import BuiltinRegistry
from ..errors import DatarError


@BuiltinRegistry.register("fetch")
def fetch(url: str) -> str:
    if not isinstance(url, str):
        raise DatarError("fetch: URL must be a string")
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.URLError as e:
        raise DatarError(f"Network error: {e.reason}")
    except Exception as e:
        raise DatarError(f"HTTP request failed: {str(e)}")


@BuiltinRegistry.register("post")
def post(data: Any, url: str, headers: Any = None) -> str:
    """
    Make HTTP POST request.

    Args:
        data: Request body (string or dict)
        url: URL to POST to
        headers: Headers as dict OR JSON string

    Returns:
        Response body as string
    """
    if not isinstance(url, str):
        raise DatarError("post: URL must be a string")

    data_str = str(data) if data is not None else ""
    req_headers = {"User-Agent": "DatarScript/1.0", "Content-Type": "application/json"}

    if headers:
        if isinstance(headers, dict):
            req_headers.update(headers)
        elif isinstance(headers, str):
            # Try to parse headers as JSON string
            try:
                hdr_dict = json.loads(headers)
                if isinstance(hdr_dict, dict):
                    for key, value in hdr_dict.items():
                        req_headers[str(key)] = str(value)
            except json.JSONDecodeError as e:
                raise DatarError(f"Invalid headers JSON: {e}")

    req = urllib.request.Request(
        url,
        data=data_str.encode("utf-8"),
        headers=req_headers,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        raise DatarError(f"HTTP {e.code}: {error_body}")
    except urllib.error.URLError as e:
        raise DatarError(f"Network error: {e.reason}")
    except Exception as e:
        raise DatarError(f"HTTP POST failed: {str(e)}")


@BuiltinRegistry.register("json_parse")
def json_parse(json_str: str) -> Any:
    if not isinstance(json_str, str):
        raise DatarError("json_parse: input must be a string")
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise DatarError(f"JSON parse error: {e.msg}")


@BuiltinRegistry.register("json_encode")
def json_encode(value: Any) -> str:
    try:
        return json.dumps(value)
    except (TypeError, ValueError) as e:
        raise DatarError(f"JSON encode error: {str(e)}")
