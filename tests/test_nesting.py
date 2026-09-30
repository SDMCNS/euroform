"""Tests for point nesting and regrouping algorithms."""
from __future__ import annotations

from euroform.nesting import (
    _point_token,
    _signature,
    _wrap_of,
    group_points,
)


def test_point_token():
    assert _point_token("(1)") == "1"
    assert _point_token("1.") == "1"
    assert _point_token("(a)") == "a"
    assert _point_token("(iv)") == "iv"
    assert _point_token("  (12a)  ") == "12a"


def test_wrap_of():
    assert _wrap_of("(1)") == "paren"
    assert _wrap_of("1)") == "close"
    assert _wrap_of("1.") == "dot"
    assert _wrap_of("1") == "bare"


def test_signature():
    assert _signature("(1)", []) == ("num", "paren", "1")
    assert _signature("(a)", []) == ("alpha", "paren", "a")
    assert _signature("(i)", []) == ("roman", "paren", "i")
    # Disambiguation: after (h), (i) is alpha
    stack = [(("alpha", "paren", "h"), "h")]
    assert _signature("(i)", stack) == ("alpha", "paren", "i")


def test_group_points_hierarchy():
    blocks = [
        {"type": "item", "number": "(1)", "text": "First point"},
        {"type": "item", "number": "(a)", "text": "Sub point a"},
        {"type": "item", "number": "(i)", "text": "Sub sub point i"},
        {"type": "item", "number": "(ii)", "text": "Sub sub point ii"},
        {"type": "item", "number": "(b)", "text": "Sub point b"},
        {"type": "item", "number": "(2)", "text": "Second point"},
    ]
    grouped = group_points(blocks)
    assert len(grouped) == 2
    p1, p2 = grouped[0], grouped[1]
    assert p1["number"] == "(1)"
    assert p2["number"] == "(2)"

    assert "content" in p1
    # p1 content has (a) and (b)
    p1_children = p1["content"]
    # first element might be preserved text if converted, let's find (a) and (b)
    sub_a = next(c for c in p1_children if c.get("number") == "(a)")
    sub_b = next(c for c in p1_children if c.get("number") == "(b)")
    assert sub_a and sub_b

    # sub_a content has (i) and (ii)
    assert "content" in sub_a
    assert any(c.get("number") == "(i)" for c in sub_a["content"])
    assert any(c.get("number") == "(ii)" for c in sub_a["content"])
