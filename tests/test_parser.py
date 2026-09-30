"""Tests for euroform core parser."""
from __future__ import annotations

import io
import json
from pathlib import Path

import pytest
from euroform.parser import FormexParser, formex_to_json, formex_to_text, parse_formex


def test_parse_basic_act_str(basic_act_xml: str):
    doc = parse_formex(basic_act_xml)
    assert doc["format"] == "formex"
    assert doc["root"] == "ACT"
    assert "Regulation (EU) 2024/123" in doc["title"]
    assert doc["subtitle"] == "on standard artificial intelligence safety frameworks"

    # Metadata
    meta = doc["metadata"]
    assert meta["language"] == "EN"
    assert meta["date"] == "2024-02-15"
    assert meta["document_type"] == "REG"
    assert meta["eea_relevance"] is True
    assert meta["official_journal"]["number"] == "042"
    assert meta["official_journal"]["year"] == "2024"

    # Preamble
    pre = doc["preamble"]
    assert "EUROPEAN PARLIAMENT" in pre["initial"]
    assert len(pre["visas"]) == 1
    assert "Article 114" in pre["visas"][0]
    assert len(pre["recitals"]) == 2
    assert pre["recitals"][0]["number"] == "(1)"
    assert pre["final"] == "HAVE ADOPTED THIS REGULATION:"

    # Body
    body = doc["body"]
    assert len(body) == 1
    article = body[0]
    assert article["type"] == "article"
    assert article["number"] == "Article 1"
    assert article["subtitle"] == "Subject matter and scope"
    assert article["identifier"] == "001"

    # Final
    final = doc["final"]
    assert "content" in final
    sig = final["content"][0]
    assert sig["type"] == "signature"
    assert "15 February 2024" in sig["place_and_date"]
    assert len(sig["signatories"]) == 2


def test_parse_bytes_and_file_like(basic_act_xml: str, tmp_path: Path):
    # From bytes
    raw_bytes = basic_act_xml.encode("utf-8")
    doc_bytes = parse_formex(raw_bytes)
    assert doc_bytes["title"] == parse_formex(basic_act_xml)["title"]

    # From BytesIO
    doc_bio = parse_formex(io.BytesIO(raw_bytes))
    assert doc_bio["title"] == doc_bytes["title"]

    # From StringIO
    doc_sio = parse_formex(io.StringIO(basic_act_xml))
    assert doc_sio["title"] == doc_bytes["title"]

    # From file Path
    fpath = tmp_path / "test.fmx.xml"
    fpath.write_text(basic_act_xml, encoding="utf-8")
    doc_path = parse_formex(fpath)
    assert doc_path["title"] == doc_bytes["title"]


def test_table_and_math_parsing(table_act_xml: str):
    doc = parse_formex(table_act_xml)
    article = doc["body"][0]
    # Check table
    tbl = next(b for b in article["content"] if b["type"] == "table")
    assert tbl["title"] == "Threshold Values"
    assert tbl["columns"] == 3
    assert len(tbl["header"]) == 1
    assert tbl["header"][0] == ["Parameter", "Limit", "Unit"]
    assert tbl["rows"][0][0] == "Mass concentration"
    assert tbl["rows"][0][2] == "mg/m³"  # EXPONENT rendered as superscript
    assert len(tbl["spans"]) == 1
    assert tbl["spans"][0]["colspan"] == 2

    # Check fraction and root
    parag = next(b for b in article["content"] if b["type"] == "paragraph")
    assert "(a + b)/c" in parag["text"]
    assert "³√(x)" in parag["text"]


def test_notes_and_anonymisation(notes_act_xml: str):
    doc = parse_formex(notes_act_xml)
    assert doc.get("anonymised") is True
    assert "notes" in doc
    assert "E0001" in doc["notes"]
    assert "OJ L 55" in doc["notes"]["E0001"]

    body_text = doc["body"][0]["content"][0]["text"]
    assert "[^E0001]" in body_text
    assert "[Company X]" in body_text


def test_formex_to_json_helper(basic_act_xml: str):
    json_str = formex_to_json(basic_act_xml, indent=2)
    assert isinstance(json_str, str)
    parsed = json.loads(json_str)
    assert parsed["format"] == "formex"
    assert "metadata" in parsed


def test_formex_to_text_helper(basic_act_xml: str):
    text = formex_to_text(basic_act_xml)
    assert isinstance(text, str)
    assert "Regulation (EU) 2024/123" in text
    assert "Article 1" in text
    assert "Done at Brussels" in text


def test_options_metadata_flag(basic_act_xml: str):
    doc = parse_formex(basic_act_xml, include_metadata=False)
    assert "metadata" not in doc
    assert "title" in doc


def test_options_nest_points_flag(nesting_act_xml: str):
    doc_nested = parse_formex(nesting_act_xml, nest_points=True)
    doc_flat = parse_formex(nesting_act_xml, nest_points=False)

    # In nested, sub-points are inside paragraph content
    article_nested = doc_nested["body"][0]
    p1_nested = article_nested["content"][0]
    assert "content" in p1_nested
    assert any(b.get("number") == "(a)" for b in p1_nested["content"])

    # In flat, points remain top-level children of article
    article_flat = doc_flat["body"][0]
    p1_flat = article_flat["content"][0]
    assert "content" not in p1_flat
    assert any(b.get("number") == "(a)" for b in article_flat["content"])
