from __future__ import annotations

import io

import pikepdf
import pytest

from pipeline.artifacts import MediaTypeMismatch, prepare_artifact


def pdf_with_forbidden_metadata() -> bytes:
    pdf = pikepdf.Pdf.new()
    pdf.add_blank_page()
    pdf.docinfo["/Author"] = "REMOVE_ME"
    pdf.docinfo["/Creator"] = "REMOVE_ME"
    pdf.docinfo["/Producer"] = "REMOVE_ME"
    with pdf.open_metadata(set_pikepdf_as_editor=False) as metadata:
        metadata["dc:creator"] = ["REMOVE_ME"]
        metadata["xmp:CreatorTool"] = "REMOVE_ME"
        metadata["pdf:Producer"] = "REMOVE_ME"
    pdf.docinfo["/CreationDate"] = "D:20251014143825+02'00'"
    pdf.docinfo["/ModDate"] = "D:20251014144000+02'00'"
    output = io.BytesIO()
    pdf.save(output)
    return output.getvalue()


def test_pdf_transform_strips_object_metadata_and_preserves_timestamps_separately() -> None:
    prepared = prepare_artifact(pdf_with_forbidden_metadata(), "application/pdf")

    assert prepared.hashes.pre_transform_response_hash != prepared.hashes.stored_content_hash
    assert prepared.extracted_pdf_timestamps is not None
    assert prepared.extracted_pdf_timestamps.creation_date == "D:20251014143825+02'00'"
    assert prepared.transform.checks == (
        "reparse_succeeded",
        "forbidden_metadata_absent",
        "byte_idempotent",
    )
    with pikepdf.Pdf.open(io.BytesIO(prepared.stored_bytes)) as reparsed:
        assert "/Info" not in reparsed.trailer
        assert all(
            not any(key in obj for key in ("/Author", "/Creator", "/Producer", "/Metadata"))
            for obj in reparsed.objects
            if isinstance(obj, pikepdf.Dictionary)
        )


def test_pdf_transform_is_byte_idempotent() -> None:
    first = prepare_artifact(pdf_with_forbidden_metadata(), "application/pdf")
    second = prepare_artifact(first.stored_bytes, "application/pdf")

    assert second.stored_bytes == first.stored_bytes
    assert second.hashes.pre_transform_response_hash == first.hashes.stored_content_hash


def test_html_is_an_exact_identity_transform_with_two_equal_hashes() -> None:
    content = b"<p>Baubeginn\r\n2026</p>"
    prepared = prepare_artifact(content, "text/html; charset=utf-8")

    assert prepared.stored_bytes == content
    assert prepared.hashes.pre_transform_response_hash == prepared.hashes.stored_content_hash
    assert prepared.transform.rule_version == "identity/v1"


def test_pdf_bytes_cannot_bypass_the_pdf_transform() -> None:
    with pytest.raises(MediaTypeMismatch):
        prepare_artifact(pdf_with_forbidden_metadata(), "text/html")
