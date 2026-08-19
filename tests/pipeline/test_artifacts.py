from __future__ import annotations

import io

import pikepdf
import pytest

from pipeline.artifacts import (
    EmbeddedFileNotPermitted,
    MalformedPdf,
    MediaTypeMismatch,
    UnsupportedMediaType,
    prepare_artifact,
)


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
        "embedded_files_absent",
        "byte_idempotent",
    )
    with pikepdf.Pdf.open(io.BytesIO(prepared.stored_bytes)) as reparsed:
        assert "/Info" not in reparsed.trailer
        assert all(
            not any(key in obj for key in ("/Author", "/Creator", "/Producer", "/Metadata"))
            for obj in reparsed.objects
            if isinstance(obj, pikepdf.Dictionary)
        )


def test_stripped_pdf_contains_no_trace_of_the_forbidden_values() -> None:
    """Key-absence is not enough: the value must be gone from the retained bytes."""

    prepared = prepare_artifact(pdf_with_forbidden_metadata(), "application/pdf")

    assert b"REMOVE_ME" not in prepared.stored_bytes
    with pikepdf.Pdf.open(io.BytesIO(prepared.stored_bytes)) as reparsed:
        assert dict(reparsed.open_metadata()) == {}
        for obj in reparsed.objects:
            if isinstance(obj, pikepdf.Stream):
                assert b"REMOVE_ME" not in bytes(obj.read_bytes())


def test_pdf_with_a_second_reference_to_info_is_still_stripped() -> None:
    pdf = pikepdf.Pdf.new()
    pdf.add_blank_page()
    pdf.docinfo["/Author"] = "SECOND_REF_AUTHOR"
    pdf.Root["/AlsoInfo"] = pdf.trailer["/Info"]
    output = io.BytesIO()
    pdf.save(output)

    prepared = prepare_artifact(output.getvalue(), "application/pdf")

    assert b"SECOND_REF_AUTHOR" not in prepared.stored_bytes


def test_embedded_file_reference_is_stripped_from_retained_bytes() -> None:
    """Attachment names are neither document metadata nor body text; rule 3 still applies."""

    pdf = pikepdf.Pdf.new()
    pdf.add_blank_page()
    filespec = pikepdf.Dictionary(
        Type=pikepdf.Name("/Filespec"), F=pikepdf.String("draft_by_EMBEDDED_NAME.docx")
    )
    pdf.Root["/Names"] = pdf.make_indirect(
        pikepdf.Dictionary(
            EmbeddedFiles=pikepdf.Dictionary(
                Names=pikepdf.Array([pikepdf.String("a"), pdf.make_indirect(filespec)])
            )
        )
    )
    output = io.BytesIO()
    pdf.save(output)

    prepared = prepare_artifact(output.getvalue(), "application/pdf")
    assert b"EMBEDDED_NAME" not in prepared.stored_bytes


def test_embedded_file_surviving_the_strip_blocks_retention() -> None:
    pdf = pikepdf.Pdf.new()
    pdf.add_blank_page()
    pdf.Root["/Keep"] = pdf.make_indirect(
        pikepdf.Dictionary(Type=pikepdf.Name("/Filespec"), F=pikepdf.String("EMBEDDED_NAME.docx"))
    )
    output = io.BytesIO()
    pdf.save(output)

    with pytest.raises(EmbeddedFileNotPermitted):
        prepare_artifact(output.getvalue(), "application/pdf")


def test_encrypted_pdf_is_refused() -> None:
    pdf = pikepdf.Pdf.new()
    pdf.add_blank_page()
    output = io.BytesIO()
    pdf.save(output, encryption=pikepdf.Encryption(owner="o", user=""))

    with pytest.raises(MalformedPdf):
        prepare_artifact(output.getvalue(), "application/pdf")


def test_pdf_without_document_information_is_not_given_one() -> None:
    pdf = pikepdf.Pdf.new()
    pdf.add_blank_page()
    output = io.BytesIO()
    pdf.save(output)

    prepared = prepare_artifact(output.getvalue(), "application/pdf")

    assert prepared.extracted_pdf_timestamps == prepared.extracted_pdf_timestamps
    with pikepdf.Pdf.open(io.BytesIO(prepared.stored_bytes)) as reparsed:
        assert "/Info" not in reparsed.trailer


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


def test_media_type_absent_from_the_configured_transforms_is_refused() -> None:
    with pytest.raises(UnsupportedMediaType):
        prepare_artifact(b"<p>x</p>", "text/html", transforms={"application/pdf": "pdf-metadata-strip/v1"})
