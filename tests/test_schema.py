"""Tests for JSON Schema generation."""
from __future__ import annotations

import json
from euroform.schema import build_schema


def test_build_schema():
    schema = build_schema()
    assert isinstance(schema, dict)
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
    assert "properties" in schema
    assert "format" in schema["properties"]
    assert "root" in schema["properties"]
    assert "metadata" in schema["properties"]
    assert "$defs" in schema
    assert "block" in schema["$defs"]
    assert "article" in schema["$defs"]
    assert "table" in schema["$defs"]

    # Verify JSON serializable
    dumped = json.dumps(schema)
    assert len(dumped) > 100
