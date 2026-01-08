# Copyright (c) Microsoft. All rights reserved.

"""
Trace Processors
"""

from .span_processor import SpanProcessor

# Export public API
__all__ = [
    # Span processor
    "SpanProcessor",
]
