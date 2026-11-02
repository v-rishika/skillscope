from pypdf import PdfReader
from docx import Document


def extract_text_from_pdf(file):
    """Extract selectable text from a PDF."""

    reader = PdfReader(file)

    pages = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            pages.append(page_text.strip())

    return "\n".join(pages).strip()


def extract_text_from_docx(file):
    """Extract text from DOCX paragraphs, tables, headers and footers."""

    document = Document(file)

    text_parts = []

    # Normal paragraphs
    for paragraph in document.paragraphs:
        content = paragraph.text.strip()

        if content:
            text_parts.append(content)

    # Tables
    for table in document.tables:
        for row in table.rows:
            cells = []

            for cell in row.cells:
                content = cell.text.strip()

                if content:
                    cells.append(content)

            if cells:
                text_parts.append(" | ".join(cells))

    # Headers and footers
    for section in document.sections:

        for paragraph in section.header.paragraphs:
            content = paragraph.text.strip()

            if content:
                text_parts.append(content)

        for paragraph in section.footer.paragraphs:
            content = paragraph.text.strip()

            if content:
                text_parts.append(content)

    # Remove duplicate consecutive content
    cleaned = []
    seen = set()

    for item in text_parts:
        normalized = item.casefold()

        if normalized not in seen:
            cleaned.append(item)
            seen.add(normalized)

    return "\n".join(cleaned).strip()


def extract_resume_text(file):
    """Extract text from PDF or DOCX files."""

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        text = extract_text_from_pdf(file)

    elif file_name.endswith(".docx"):
        text = extract_text_from_docx(file)

    else:
        raise ValueError(
            "Unsupported file type. Please upload a PDF or DOCX file."
        )

    if not text.strip():
        raise ValueError(
            "We couldn't extract readable text from this file. "
            "If this is a scanned PDF, please paste the job description "
            "or upload a text-based DOCX/PDF."
        )

    return text.strip()