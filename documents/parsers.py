import io
import re
from decimal import Decimal
from typing import Optional, Tuple

from dateparser import parse as parse_date


def _safe_decimal(num_str: str) -> Optional[Decimal]:
	try:
		num_str = num_str.replace(',', '').strip()
		return Decimal(num_str)
	except Exception:
		return None


def extract_text_from_pdf(django_file) -> str:
	"""Try to extract text from a PDF using pdfplumber if available.
	Returns empty string on failure.
	"""
	try:
		import pdfplumber  # type: ignore
		data = django_file.read()
		django_file.seek(0)
		buf = io.BytesIO(data)
		text_parts = []
		with pdfplumber.open(buf) as pdf:
			for page in pdf.pages:
				text_parts.append(page.extract_text() or "")
		return "\n".join(text_parts)
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
	amount_patterns = [
		r"(?i)(total|amount due|balance due)\D{0,20}([\d.,]+)",
		r"(?i)grand\s*total\D{0,20}([\d.,]+)",
	]
	for pat in amount_patterns:
		m = re.search(pat, text)
		if m:
			amt = _safe_decimal(m.group(m.lastindex))
			if amt is not None:
				break
	else:
		amt = None
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


