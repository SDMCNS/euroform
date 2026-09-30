"""Tests for euroform CLI interface."""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

from euroform.cli import main


def test_cli_schema(capsys):
    rc = main(["--schema"])
    assert rc == 0
    captured = capsys.readouterr()
    schema = json.loads(captured.out)
    assert schema["title"] == "Parsed Formex document"


def test_cli_version(capsys):
    rc = main(["--version"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "euroform 0.1.0" in captured.out


def test_cli_file_to_stdout(basic_act_xml: str, tmp_path: Path, capsys):
    fpath = tmp_path / "act.xml"
    fpath.write_text(basic_act_xml, encoding="utf-8")

    rc = main([str(fpath)])
    assert rc == 0
    captured = capsys.readouterr()
    doc = json.loads(captured.out)
    assert "Regulation (EU) 2024/123" in doc["title"]


def test_cli_file_output(basic_act_xml: str, tmp_path: Path):
    fpath = tmp_path / "act.xml"
    fpath.write_text(basic_act_xml, encoding="utf-8")
    out_path = tmp_path / "output.json"

    rc = main([str(fpath), "-o", str(out_path)])
    assert rc == 0
    assert out_path.exists()
    doc = json.loads(out_path.read_text(encoding="utf-8"))
    assert doc["root"] == "ACT"


def test_cli_text_flag(basic_act_xml: str, tmp_path: Path, capsys):
    fpath = tmp_path / "act.xml"
    fpath.write_text(basic_act_xml, encoding="utf-8")

    rc = main([str(fpath), "--text"])
    assert rc == 0
    captured = capsys.readouterr()
    assert "Regulation (EU) 2024/123" in captured.out
    assert "Article 1" in captured.out


def test_legacy_formex_to_json_main(basic_act_xml: str, tmp_path: Path, capsys):
    fpath = tmp_path / "act.xml"
    fpath.write_text(basic_act_xml, encoding="utf-8")

    rc = formex_to_json.main([str(fpath)])
    assert rc == 0
    captured = capsys.readouterr()
    doc = json.loads(captured.out)
    assert doc["root"] == "ACT"
