"""
Medical Test Simplifier
-----------------------
Reads a PDF containing medical test results and uses a local
Ollama LLM to explain them in plain, easy-to-understand English.

Usage:
    python main.py <path_to_pdf>
    python main.py <path_to_pdf> --model llama3.2
    python main.py <path_to_pdf> --model llama3.2 --save
"""

import argparse
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("❌ Missing dependency: PyMuPDF\n   Run: pip install pymupdf")
    sys.exit(1)

try:
    import ollama
except ImportError:
    print("❌ Missing dependency: ollama\n   Run: pip install ollama")
    sys.exit(1)


# ──────────────────────────────────────────────
# PDF Extraction
# ──────────────────────────────────────────────

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file."""
    path = Path(pdf_path)
    if not path.exists():
        print(f"❌ File not found: {pdf_path}")
        sys.exit(1)
    if path.suffix.lower() != ".pdf":
        print("❌ Please provide a .pdf file.")
        sys.exit(1)

    doc = fitz.open(str(path))
    pages_text = []
    for i, page in enumerate(doc):
        text = page.get_text().strip()
        if text:
            pages_text.append(f"[Page {i + 1}]\n{text}")
    doc.close()

    combined = "\n\n".join(pages_text)
    if not combined.strip():
        print("❌ No readable text found. The PDF may be a scanned image.")
        print("   Try converting it to a text-based PDF first.")
        sys.exit(1)

    return combined


# ──────────────────────────────────────────────
# LLM Simplification
# ──────────────────────────────────────────────

SYSTEM_PROMPT = """You are a friendly and knowledgeable medical assistant.
Your job is to take medical lab test results and explain them in simple,
clear language that a patient with no medical background can understand.

When you see test results, always:
1. Explain what each test is measuring in plain English
2. State whether the result is Normal, High, or Low
3. Describe what that result means for the patient's health
4. Highlight anything that might need attention (but avoid causing unnecessary alarm)
5. End with a brief friendly summary

Keep your tone warm, clear, and reassuring. Avoid medical jargon — if you
must use a medical term, immediately explain it in simple words."""


def simplify_medical_text(text: str, model: str) -> str:
    """Send extracted PDF text to Ollama and get a plain-English explanation."""
    user_message = f"""Please simplify the following medical test results into plain English:

---
{text}
---

Remember to explain each test, its result (Normal / High / Low), and what it means in simple terms."""

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
        )
        return response["message"]["content"]
    except ollama.ResponseError as e:
        print(f"\n❌ Ollama error: {e}")
        print(f"   Make sure the model '{model}' is pulled. Run:\n   ollama pull {model}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Could not connect to Ollama: {e}")
        print("   Make sure Ollama is running: https://ollama.com")
        sys.exit(1)


# ──────────────────────────────────────────────
# Output
# ──────────────────────────────────────────────

def print_result(simplified: str, pdf_path: str, save: bool):
    """Print the simplified result and optionally save it to a file."""
    border = "=" * 64
    print(f"\n{border}")
    print("  📋  SIMPLIFIED MEDICAL RESULTS")
    print(f"{border}\n")
    print(simplified)
    print(f"\n{border}")

    if save:
        output_path = Path(pdf_path).with_stem(Path(pdf_path).stem + "_simplified").with_suffix(".txt")
        output_path.write_text(simplified, encoding="utf-8")
        print(f"\n💾 Saved to: {output_path}")


# ──────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Simplify medical test results from a PDF using a local LLM (Ollama).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py results.pdf
  python main.py results.pdf --model llama3.2
  python main.py results.pdf --model mistral --save
        """,
    )
    parser.add_argument("pdf", help="Path to the PDF with medical test results")
    parser.add_argument(
        "--model",
        default="llama3.2",
        help="Ollama model name to use (default: llama3.2)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the simplified output as a .txt file next to the PDF",
    )

    args = parser.parse_args()

    print(f"\n📄 Reading PDF: {args.pdf}")
    text = extract_text_from_pdf(args.pdf)
    print(f"   ✅ Extracted text from PDF ({len(text)} characters)")

    print(f"\n🤖 Sending to Ollama model '{args.model}'...")
    print("   (This may take a moment depending on your hardware)\n")
    simplified = simplify_medical_text(text, args.model)

    print_result(simplified, args.pdf, args.save)


if __name__ == "__main__":
    main()
