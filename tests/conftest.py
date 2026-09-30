"""Test fixtures and sample Formex XML snippets."""
from __future__ import annotations

import pytest

SAMPLE_BASIC_ACT = """<?xml version="1.0" encoding="utf-8"?>
<ACT xmlns:fmx="http://formex.publications.europa.eu">
  <BIB.INSTANCE>
    <DOCUMENT.REF>
      <COLL>L</COLL>
      <NO.OJ>042</NO.OJ>
      <YEAR>2024</YEAR>
      <LG.OJ>EN</LG.OJ>
    </DOCUMENT.REF>
    <LG.DOC>EN</LG.DOC>
    <DOC.TYPE>REG</DOC.TYPE>
    <DATE ISO="20240215">15.2.2024</DATE>
    <NO.DOC FORMAT="NY" TYPE="OJ">
      <NO.CURRENT>123</NO.CURRENT>
      <YEAR>2024</YEAR>
      <COM>EU</COM>
    </NO.DOC>
    <EEA/>
  </BIB.INSTANCE>
  <TITLE>
    <TI><P>Regulation (EU) 2024/123 of the European Parliament and of the Council</P></TI>
    <STI><P>on standard artificial intelligence safety frameworks</P></STI>
  </TITLE>
  <PREAMBLE>
    <PREAMBLE.INIT>THE EUROPEAN PARLIAMENT AND THE COUNCIL OF THE EUROPEAN UNION,</PREAMBLE.INIT>
    <GR.VISA>
      <VISA>Having regard to the Treaty on the Functioning of the European Union, and in particular Article 114 thereof,</VISA>
    </GR.VISA>
    <GR.CONSID>
      <GR.CONSID.INIT>Whereas:</GR.CONSID.INIT>
      <CONSID>
        <NP>
          <NO.P>(1)</NO.P>
          <TXT>The purpose of this Regulation is to improve the functioning of the internal market.</TXT>
        </NP>
      </CONSID>
      <CONSID>
        <NP>
          <NO.P>(2)</NO.P>
          <TXT>High safety benchmarks must be respected across the Union.</TXT>
        </NP>
      </CONSID>
    </GR.CONSID>
    <PREAMBLE.FINAL>HAVE ADOPTED THIS REGULATION:</PREAMBLE.FINAL>
  </PREAMBLE>
  <ENACTING.TERMS>
    <ARTICLE IDENTIFIER="001">
      <TI.ART>Article 1</TI.ART>
      <STI.ART>Subject matter and scope</STI.ART>
      <PARAG IDENTIFIER="001.001">
        <NO.PARAG>1.</NO.PARAG>
        <ALINEA>This Regulation lays down harmonised rules for AI systems.</ALINEA>
      </PARAG>
      <PARAG IDENTIFIER="001.002">
        <NO.PARAG>2.</NO.PARAG>
        <ALINEA>It applies to:</ALINEA>
        <LIST TYPE="alpha">
          <ITEM>
            <NP><NO.P>(a)</NO.P><TXT>providers placing AI on the market;</TXT></NP>
          </ITEM>
          <ITEM>
            <NP><NO.P>(b)</NO.P><TXT>deployers of AI systems in the Union.</TXT></NP>
          </ITEM>
        </LIST>
      </PARAG>
    </ARTICLE>
  </ENACTING.TERMS>
  <FINAL>
    <SIGNATURE>
      <PL.DATE>Done at Brussels, 15 February 2024.</PL.DATE>
      <SIGNATORY><P>For the European Parliament</P><P>The President</P></SIGNATORY>
      <SIGNATORY><P>For the Council</P><P>The President</P></SIGNATORY>
    </SIGNATURE>
  </FINAL>
</ACT>
"""

SAMPLE_TABLE_ACT = """<?xml version="1.0" encoding="utf-8"?>
<ACT>
  <TITLE><TI><P>Act with Table and Math</P></TI></TITLE>
  <ENACTING.TERMS>
    <ARTICLE IDENTIFIER="001">
      <TI.ART>Article 1</TI.ART>
      <TBL COLS="3">
        <TITLE><TI><P>Threshold Values</P></TI></TITLE>
        <CORPUS>
          <ROW TYPE="HEADER">
            <CELL COL="1"><HT TYPE="BOLD">Parameter</HT></CELL>
            <CELL COL="2"><HT TYPE="BOLD">Limit</HT></CELL>
            <CELL COL="3"><HT TYPE="BOLD">Unit</HT></CELL>
          </ROW>
          <ROW>
            <CELL COL="1">Mass concentration</CELL>
            <CELL COL="2">50</CELL>
            <CELL COL="3">mg/m<EXPONENT>3</EXPONENT></CELL>
          </ROW>
          <ROW>
            <CELL COL="1" COLSPAN="2">Total index</CELL>
            <CELL COL="3">1.5</CELL>
          </ROW>
        </CORPUS>
      </TBL>
      <PARAG IDENTIFIER="001.001">
        <NO.PARAG>1.</NO.PARAG>
        <ALINEA>The formula is <FRACTION><DIVIDEND>a + b</DIVIDEND><DIVISOR>c</DIVISOR></FRACTION> with root <ROOT><DEGREE>3</DEGREE>x</ROOT>.</ALINEA>
      </PARAG>
    </ARTICLE>
  </ENACTING.TERMS>
</ACT>
"""

SAMPLE_NOTES_ACT = """<?xml version="1.0" encoding="utf-8"?>
<ACT>
  <TITLE><TI><P>Act with Footnotes and Anonymisation</P></TI></TITLE>
  <ENACTING.TERMS>
    <ARTICLE IDENTIFIER="001">
      <TI.ART>Article 1</TI.ART>
      <PARAG IDENTIFIER="001.001">
        <NO.PARAG>1.</NO.PARAG>
        <ALINEA>Subject to Regulation (EU) No 182/2011<NOTE NOTE.ID="E0001"><P>OJ L 55, 28.2.2011, p. 13.</P></NOTE> and anonymised entity <ANONYMOUS PLACEHOLDER="[Company X]"/>.</ALINEA>
      </PARAG>
    </ARTICLE>
  </ENACTING.TERMS>
</ACT>
"""

SAMPLE_NESTING_ACT = """<?xml version="1.0" encoding="utf-8"?>
<ACT>
  <TITLE><TI><P>Act with Hierarchical Points</P></TI></TITLE>
  <ENACTING.TERMS>
    <ARTICLE IDENTIFIER="001">
      <TI.ART>Article 1</TI.ART>
      <PARAG IDENTIFIER="001.001">
        <NO.PARAG>1.</NO.PARAG>
        <ALINEA>First level</ALINEA>
      </PARAG>
      <ITEM><NP><NO.P>(a)</NO.P><TXT>Sub point a</TXT></NP></ITEM>
      <ITEM><NP><NO.P>(i)</NO.P><TXT>Roman sub point i</TXT></NP></ITEM>
      <ITEM><NP><NO.P>(ii)</NO.P><TXT>Roman sub point ii</TXT></NP></ITEM>
      <ITEM><NP><NO.P>(b)</NO.P><TXT>Sub point b</TXT></NP></ITEM>
      <PARAG IDENTIFIER="001.002">
        <NO.PARAG>2.</NO.PARAG>
        <ALINEA>Second numbered paragraph</ALINEA>
      </PARAG>
    </ARTICLE>
  </ENACTING.TERMS>
</ACT>
"""

INVALID_XML = "<ACT><TITLE><TI><P>Unclosed tag</ACT>"


@pytest.fixture
def basic_act_xml() -> str:
    return SAMPLE_BASIC_ACT


@pytest.fixture
def table_act_xml() -> str:
    return SAMPLE_TABLE_ACT


@pytest.fixture
def notes_act_xml() -> str:
    return SAMPLE_NOTES_ACT


@pytest.fixture
def nesting_act_xml() -> str:
    return SAMPLE_NESTING_ACT


@pytest.fixture
def invalid_xml() -> str:
    return INVALID_XML
