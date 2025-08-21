import os
import sys
from typing import Callable, Dict, List, Any
from pypdf import PdfReader


def get_base_dir() -> str:
	"""Get the correct base directory for MSIX or dev environment."""
	if getattr(sys, 'frozen', False):  # Running as MSIX/compiled
		return os.path.dirname(sys.executable)
	return os.path.dirname(os.path.abspath(__file__))


class PDFTextImageExtractorPypdf:
	"""Extract text content from PDF using pypdf and save in the same
	markdown format produced by PDFTextImageExtractor in pdf_reader.py.
	
	- Matches the JSON structure returned by extract_full_content()
	- Matches save_to_markdown() section layout
	- Images are not analyzed here; the 'images' list per page is left empty
	"""

	def __init__(self) -> None:
		self.base_dir = get_base_dir()

	def extract_full_content(
		self,
		pdf_path: str,
		output_dir: str = "output",
		status_callback: Callable[[Dict[str, Any]], None] | None = None,
	) -> Dict[str, Any]:
		os.makedirs(output_dir, exist_ok=True)

		reader = PdfReader(pdf_path)
		num_pages = len(reader.pages)

		if status_callback:
			status_callback({
				'type': 'status',
				'message': f"PDF loaded successfully. Total pages: {num_pages}"
			})

		full_content: Dict[str, Any] = {
			'metadata': {
				'source': os.path.basename(pdf_path),
				'total_pages': num_pages,
			},
			'pages': []
		}

		for page_num in range(num_pages):
			if status_callback:
				status_callback({
					'type': 'status',
					'message': f"Processing page {page_num + 1}/{num_pages}..."
				})

			page = reader.pages[page_num]
			try:
				text = page.extract_text() or ""
			except Exception:
				text = ""

			page_content = {
				'page_number': page_num + 1,
				'text': text,
				'images': [],          # Keep schema compatibility
				'tables': [],          # Placeholder for schema compatibility
			}

			full_content['pages'].append(page_content)

			if status_callback:
				status_callback({
					'type': 'status',
					'message': f"Page {page_num + 1} processed - {len(text)} chars, 0 images"
				})

		return full_content

	def save_to_markdown(self, content: Dict[str, Any], output_path: str) -> None:
		"""Save results to markdown file (same formatting as pdf_reader.py)."""
		with open(output_path, "w", encoding="utf-8") as f:
			f.write(f"# Complete Extraction from: {content['metadata']['source']}\n\n")
			f.write(f"**Total Pages:** {content['metadata']['total_pages']}\n\n")

			for page in content['pages']:
				f.write(f"\n\n## Page {page['page_number']}\n\n")
				f.write((page.get('text') or "") + "\n\n")

				# Keep the image section parity even if empty
				for img in page.get('images', []) or []:
					f.write(f"\n### Image (Page {img.get('page', page['page_number'])})\n")
					f.write(f"**Type:** {(img.get('type') or 'unknown').title()}\n\n")
					# Minimal placeholders; this extractor does not caption images
					f.write(f"**Description:** (not available in pypdf extractor)\n\n")
					f.write(f"**Educational Analysis:** (not available in pypdf extractor)\n\n")
					f.write("**Key Concepts:** \n")

	def extract_and_save(self, pdf_path: str, output_dir: str = "output",
						  status_callback: Callable[[Dict[str, Any]], None] | None = None) -> str:
		"""End-to-end helper that writes to output/<base_name>_content.md (matches app.py/trans.py)."""
		os.makedirs(output_dir, exist_ok=True)
		content = self.extract_full_content(pdf_path, output_dir=output_dir, status_callback=status_callback)
		base_name = os.path.splitext(os.path.basename(pdf_path))[0]
		out_path = os.path.join(output_dir, f"{base_name}_content.md")
		self.save_to_markdown(content, out_path)
		return out_path


if __name__ == "__main__":
	import argparse

	parser = argparse.ArgumentParser(description="Extract PDF to markdown using pypdf")
	parser.add_argument("pdf", help="Path to input PDF")
	parser.add_argument("--out", help="Output markdown file path (overrides default)")
	parser.add_argument("--outdir", help="Output directory (default: output)", default="output")
	args = parser.parse_args()

	extractor = PDFTextImageExtractorPypdf()
	if args.out:
		# honor explicit override
		content = extractor.extract_full_content(args.pdf, output_dir=os.path.dirname(args.out) or args.outdir)
		extractor.save_to_markdown(content, args.out)
		print(f"Extraction complete. Saved to: {args.out}")
	else:
		# default naming: output/<base_name>_content.md
		out_path = extractor.extract_and_save(args.pdf, output_dir=args.outdir)
		print(f"Extraction complete. Saved to: {out_path}")

