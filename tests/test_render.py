"""Tests for text rendering module."""
from __future__ import annotations

from euroform.render import render_block, render_blocks, render_text


def test_render_blocks():
    blocks = [
        {"type": "heading", "text": "CHAPTER I", "subtitle": "GENERAL PROVISIONS"},
        {"type": "article", "number": "Article 1", "title": "Subject", "text": "This is article 1."},
        {
            "type": "list",
            "style": "bullet",
            "items": [
                {"type": "item", "text": "Item one"},
                {"type": "item", "text": "Item two"},
            ],
        },
        {
            "type": "definition_list",
            "items": [
                {"term": "AI", "definition": "Artificial Intelligence"},
            ],
        },
        {"type": "quote", "content": [{"type": "text", "text": "Quoted passage"}]},
        {"type": "annotation", "title": "Note", "text": "Editorial remark"},
        {"type": "figure", "caption": "Diagram of flow"},
        {
            "type": "signature",
            "place_and_date": "Brussels, 2024",
            "signatories": ["President A", "President B"],
        },
    ]

    rendered = render_blocks(blocks)
    assert "CHAPTER I" in rendered
    assert "GENERAL PROVISIONS" in rendered
    assert "Article 1" in rendered
    assert "- Item one" in rendered
    assert "AI: Artificial Intelligence" in rendered
    assert "> Quoted passage" in rendered
    assert "[Note] Editorial remark" in rendered
    assert "[Figure: Diagram of flow]" in rendered
    assert "Brussels, 2024" in rendered
    assert "President A" in rendered


def test_render_full_doc():
    doc = {
        "title": "Title of Regulation",
        "preamble": {
            "initial": "THE COMMISSION,",
            "visas": ["Visa 1", "Visa 2"],
            "recitals": [{"type": "item", "number": "(1)", "text": "Recital 1"}],
            "final": "HAS ADOPTED:",
        },
        "body": [
            {"type": "article", "number": "Art 1", "text": "Body text"}
        ],
        "notes": {
            "1": "Footnote text"
        }
    }
    txt = render_text(doc)
    assert "Title of Regulation" in txt
    assert "THE COMMISSION," in txt
    assert "Visa 1" in txt
    assert "(1) Recital 1" in txt
    assert "HAS ADOPTED:" in txt
    assert "Art 1" in txt
    assert "[^1] Footnote text" in txt
