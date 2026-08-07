from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass
from typing import Mapping

import pikepdf


PDF_RULE_VERSION = "pdf-metadata-strip/v1"
IDENTITY_RULE_VERSION = "identity/v1"
FORBIDDEN_KEYS = ("/Author", "/Creator", "/Producer", "/Metadata")


class ArtifactPreparationError(ValueError):
    """Stable, content-free failure raised before any artifact can be retained."""


class UnsupportedMediaType(ArtifactPreparationError):
    pass


class MediaTypeMismatch(ArtifactPreparationError):
    pass


class MalformedPdf(ArtifactPreparationError):
    pass


class TransformVerificationFailed(ArtifactPreparationError):
    pass


class NonIdempotentTransform(ArtifactPreparationError):
    pass


@dataclass(frozen=True)
class ArtifactHashes:
    pre_transform_response_hash: str
    stored_content_hash: str
    hash_algorithm: str = "sha256"


@dataclass(frozen=True)
class PdfTimestamps:
    creation_date: str | None
    modification_date: str | None


@dataclass(frozen=True)
class TransformRecord:
    rule_version: str
    checks: tuple[str, ...]
    pikepdf_version: str
    qpdf_version: str


@dataclass(frozen=True)
class PreparedArtifact:
    stored_bytes: bytes
    media_type: str
    byte_length: int
    hashes: ArtifactHashes
    transform: TransformRecord
    extracted_pdf_timestamps: PdfTimestamps | None


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _media_type(value: str) -> str:
    return value.partition(";")[0].strip().lower()


def _extract_timestamp(info: pikepdf.Dictionary, key: str) -> str | None:
    if key not in info:
        return None
    return str(info[key])


def _strip_pdf_once(content: bytes) -> tuple[bytes, PdfTimestamps]:
    try:
        pdf = pikepdf.Pdf.open(
            io.BytesIO(content),
            attempt_recovery=False,
            inherit_page_attributes=False,
        )
    except (pikepdf.PdfError, ValueError) as exc:
        raise MalformedPdf("PDF parsing failed") from exc

    try:
        if pdf.is_encrypted:
            raise MalformedPdf("encrypted PDFs are not supported")

        info = pdf.docinfo
        timestamps = PdfTimestamps(
            creation_date=_extract_timestamp(info, "/CreationDate"),
            modification_date=_extract_timestamp(info, "/ModDate"),
        )

        if "/Info" in pdf.trailer:
            del pdf.trailer["/Info"]

        for obj in pdf.objects:
            if isinstance(obj, pikepdf.Dictionary):
                for key in FORBIDDEN_KEYS:
                    if key in obj:
                        del obj[key]

        output = io.BytesIO()
        pdf.save(
            output,
            deterministic_id=True,
            fix_metadata_version=False,
            object_stream_mode=pikepdf.ObjectStreamMode.preserve,
            normalize_content=False,
            linearize=False,
        )
        return output.getvalue(), timestamps
    finally:
        pdf.close()


def _verify_pdf(content: bytes) -> None:
    try:
        pdf = pikepdf.Pdf.open(
            io.BytesIO(content),
            attempt_recovery=False,
            inherit_page_attributes=False,
        )
    except (pikepdf.PdfError, ValueError) as exc:
        raise TransformVerificationFailed("rewritten PDF did not reparse") from exc

    try:
        if "/Info" in pdf.trailer:
            raise TransformVerificationFailed("forbidden document information remains")
        for obj in pdf.objects:
            if isinstance(obj, pikepdf.Dictionary) and any(key in obj for key in FORBIDDEN_KEYS):
                raise TransformVerificationFailed("forbidden metadata remains reachable")
    finally:
        pdf.close()


def prepare_artifact(
    response_bytes: bytes,
    declared_media_type: str,
    *,
    transforms: Mapping[str, str] | None = None,
) -> PreparedArtifact:
    """Return retention-safe bytes, or fail before callers can persist anything."""

    media_type = _media_type(declared_media_type)
    looks_like_pdf = response_bytes.lstrip().startswith(b"%PDF-")
    if media_type == "application/pdf" and not looks_like_pdf:
        raise MediaTypeMismatch("declared PDF does not have PDF magic")
    if media_type != "application/pdf" and looks_like_pdf:
        raise MediaTypeMismatch("PDF bytes cannot use an identity transform")

    if transforms is not None and transforms.get(media_type) is None:
        raise UnsupportedMediaType(f"no configured transform for media type {media_type!r}")

    pre_hash = _sha256(response_bytes)
    if media_type == "text/html":
        stored = response_bytes
        timestamps = None
        rule = IDENTITY_RULE_VERSION
        checks = ("identity_hashes_equal",)
    elif media_type == "application/pdf":
        stored, timestamps = _strip_pdf_once(response_bytes)
        _verify_pdf(stored)
        second, _ = _strip_pdf_once(stored)
        _verify_pdf(second)
        if second != stored:
            raise NonIdempotentTransform("PDF transform did not reach a byte-stable result")
        rule = PDF_RULE_VERSION
        checks = ("reparse_succeeded", "forbidden_metadata_absent", "byte_idempotent")
    else:
        raise UnsupportedMediaType(f"no artifact transform for media type {media_type!r}")

    if transforms is not None and transforms[media_type] != rule:
        raise TransformVerificationFailed(
            f"configured transform {transforms[media_type]!r} does not match applied rule {rule!r}"
        )

    stored_hash = _sha256(stored)
    if rule == IDENTITY_RULE_VERSION and stored_hash != pre_hash:
        raise TransformVerificationFailed("identity transform changed content")

    return PreparedArtifact(
        stored_bytes=stored,
        media_type=media_type,
        byte_length=len(stored),
        hashes=ArtifactHashes(
            pre_transform_response_hash=pre_hash,
            stored_content_hash=stored_hash,
        ),
        transform=TransformRecord(
            rule_version=rule,
            checks=checks,
            pikepdf_version=pikepdf.__version__,
            qpdf_version=pikepdf.__libqpdf_version__,
        ),
        extracted_pdf_timestamps=timestamps,
    )
