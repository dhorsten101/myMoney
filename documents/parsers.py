import io
import re
from decimal import Decimal
from typing import Optional, Tuple, List

from dateparser import parse as parse_date


def _safe_decimal(num_str: str) -> Optional[Decimal]:
    """Convert a localized numeric string to Decimal.
    Handles formats like '1,234.56', '1 234,56', 'R 1 234,56'.
    """
    try:
        s = (num_str or "").strip()
        # Remove currency symbols and letters
        s = re.sub(r"[A-Za-zR$€£ZARzar\s\u00A0]", "", s)
        # If both ',' and '.' exist, assume ',' are thousands -> remove ','
        if "," in s and "." in s:
            s = s.replace(",", "")
        # If only ',' exists, assume it's decimal separator -> replace with '.'
        elif "," in s and "." not in s:
            s = s.replace(",", ".")
        # Remove any remaining spaces/nbsp just in case
        s = s.replace(" ", "").replace("\u00A0", "")
        return Decimal(s)
    except Exception:
        return None


def extract_text_from_pdf(django_file) -> str:
	"""Try to extract text from a PDF using pdfplumber if available.
	Returns empty string on failure.
	"""
	# Try pdfplumber first
	try:
		import pdfplumber  # type: ignore
		data = django_file.read()
		django_file.seek(0)
		buf = io.BytesIO(data)
		text_parts = []
		with pdfplumber.open(buf) as pdf:
			for page in pdf.pages:
				text_parts.append(page.extract_text() or "")
		text = "\n".join(text_parts).strip()
		if text:
			return text
	except Exception:
		pass
	# Fallback: PyPDF2 if available
	try:
		from PyPDF2 import PdfReader  # type: ignore
		data = django_file.read()
		django_file.seek(0)
		reader = PdfReader(io.BytesIO(data))
		texts = []
		for page in reader.pages:
			try:
				texts.append(page.extract_text() or "")
			except Exception:
				continue
		return "\n".join(texts).strip()
	except Exception:
		pass
	# Final fallback: render pages and OCR via PyMuPDF + pytesseract if available
	try:
		import fitz  # PyMuPDF  # type: ignore
		from PIL import Image  # type: ignore
		import pytesseract  # type: ignore
		data = django_file.read()
		django_file.seek(0)
		doc = fitz.open(stream=data, filetype="pdf")
		ocr_texts: list[str] = []
		for page in doc:
			pix = page.get_pixmap(dpi=200)
			mode = "RGBA" if pix.alpha else "RGB"
			img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
			if pix.alpha:
				img = img.convert("RGB")
			ocr_texts.append(pytesseract.image_to_string(img) or "")
		return "\n".join(ocr_texts).strip()
	except Exception:
		return ""


def extract_text_from_image(django_file) -> str:
	"""Try OCR on image using pytesseract if available. Returns empty on failure."""
	try:
		from PIL import Image  # type: ignore
		import pytesseract  # type: ignore
		data = django_file.read()
		django_file.seek(0)
		img = Image.open(io.BytesIO(data))
		return pytesseract.image_to_string(img) or ""
	except Exception:
		return ""


def parse_total_and_date(text: str) -> Tuple[Optional[Decimal], Optional[str]]:
	"""Heuristic parsing for total amount and date from plain text."""
	if not text:
		return None, None
	# Common labels for totals
	amount_patterns: List[str] = [
		r"(?i)(total\s*due|amount\s*due|balance\s*due|grand\s*total|total)\s*[:\-]?\s*[R$€£\s\u00A0]*([\d\s.,]+)",
		r"(?i)subtotal\s*[:\-]?\s*[R$€£\s\u00A0]*([\d\s.,]+)",
		# Explicit 'INVOICE TOTAL' often present in headers/tables
		r"(?is)invoice\s*total\s*[:\-]?\s*[R$€£\s\u00A0]*([\d\s.,]+)",
		# A line containing just 'TOTAL' followed by a number (possibly on next line)
		r"(?is)\btotal\b[\s:]*[R$€£\s\u00A0]*([\d\s.,]+)",
	]
	amt = None
	for pat in amount_patterns:
		m = re.search(pat, text)
		if m:
			cand = _safe_decimal(m.group(m.lastindex))
			if cand is not None and cand > 0:
				amt = cand
				break
	# Fallback: pick the largest monetary-looking token in the document (requires decimal part)
	if amt is None:
		money_regex = r"[R$€£]?\s*\d{1,3}(?:[ \u00A0\.,]\d{3})*(?:[\.,]\d{2})"
		candidates = re.findall(money_regex, text)
		best = None
		for c in candidates:
			d = _safe_decimal(c)
			if d is None:
				continue
			if best is None or d > best:
				best = d
		amt = best
	# If still none, try a two-line scan around lines containing TOTAL
	if amt is None:
		lines = text.splitlines()
		for i, line in enumerate(lines):
			low = line.lower()
			if "total" in low and "subtotal" not in low:
				peek = (lines[i] + " " + (lines[i+1] if i + 1 < len(lines) else "")).strip()
				m = re.search(r"[R$€£]?\s*([\d\s.,]{3,})", peek)
				if m:
					cand = _safe_decimal(m.group(1))
					if cand is not None and cand > 0:
						amt = cand
						break
	# Date: let dateparser find the first plausible date
	date_match = None
	for line in text.splitlines():
		parsed = parse_date(line, settings={"PREFER_DATES_FROM": "past"})
		if parsed:
			date_match = parsed.date().isoformat()
			break
	return amt, date_match


def extract_amount_and_date_from_file(django_file) -> Tuple[Optional[Decimal], Optional[str]]:
	"""Dispatch based on file extension and available libs to extract text, then parse."""
	name = (getattr(django_file, 'name', '') or '').lower()
	text = ""
	if name.endswith('.pdf'):
		text = extract_text_from_pdf(django_file)
	elif name.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif', '.tif', '.tiff', '.bmp')):
		text = extract_text_from_image(django_file)
	# As a fallback, attempt naive bytes decode
	if not text:
		try:
			data = django_file.read()
			django_file.seek(0)
			text = data.decode('utf-8', errors='ignore')
		except Exception:
			text = ""
	return parse_total_and_date(text)


