import pdfplumber
from docx import Document
from typing import Optional


class ResumeReader:
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path.lower()

    def extract_text(self) -> Optional[str]:
        if self.file_path.endswith(".pdf"):
            return self._read_pdf()

        if self.file_path.endswith(".docx"):
            return self._read_docx()

        raise ValueError("Unsupported file format. Use PDF or DOCX.")

    # ---------- PDF ----------
    def _read_pdf(self) -> str:
        text_parts = []

        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return "\n".join(text_parts)

    # ---------- DOCX ----------
    def _read_docx(self) -> str:
        doc = Document(self.file_path)
        return "\n".join([para.text for para in doc.paragraphs])