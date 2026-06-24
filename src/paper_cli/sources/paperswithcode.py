"""PapersWithCode source — search and read papers via the HuggingFace API.

NOTE: PapersWithCode (paperswithcode.com) was acquired by HuggingFace and the
original REST API now redirects to huggingface.co. This module uses the
HuggingFace Papers API as the backend for searching, fetching metadata, and
reading paper content.
"""

import io
import logging
from typing import Optional

import httpx
import requests

logger = logging.getLogger("paper_cli.paperswithcode")

HF_API = "https://huggingface.co/api"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}


async def search_papers(
    title: Optional[str] = None,
    abstract: Optional[str] = None,
    arxiv_id: Optional[str] = None,
) -> str:
    """Search for papers. Uses HuggingFace Papers API (PapersWithCode successor)."""
    # If we have an arxiv_id, fetch directly
    if arxiv_id:
        url = f"{HF_API}/papers/{arxiv_id}"
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    data = resp.json()
                    return _format_hf_paper(data)
            except Exception as e:
                return f"Error looking up paper {arxiv_id}: {e}"
        return f"Paper '{arxiv_id}' not found."

    # For title/abstract search, use HuggingFace daily papers + ArXiv as fallback
    query = title or abstract or ""
    if not query:
        return "Please provide a title, abstract, or arxiv_id to search."

    # Search recent daily papers via multiple dates
    all_papers = []
    from datetime import datetime, timedelta
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        for days_ago in range(7):
            date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
            try:
                resp = await client.get(f"{HF_API}/daily_papers?date={date}")
                if resp.status_code == 200:
                    for item in resp.json():
                        paper = item.get("paper", {})
                        paper_title = item.get("title", paper.get("title", ""))
                        if query.lower() in paper_title.lower() or (
                            abstract and query.lower() in paper.get("summary", "").lower()
                        ):
                            all_papers.append({
                                "title": paper_title,
                                "authors": [a.get("name", "") for a in paper.get("authors", []) if not a.get("hidden")],
                                "abstract": paper.get("summary", "")[:200],
                                "arxiv_id": paper.get("id", ""),
                                "url": f"https://huggingface.co/papers/{paper.get('id', '')}",
                                "upvotes": paper.get("upvotes", 0),
                            })
            except Exception:
                continue

    if not all_papers:
        return f"No papers found matching '{query}'. Try using arxiv_search or scholar_search for broader results."

    lines = [f"PapersWithCode/HuggingFace results for '{query}' — {len(all_papers)} papers:\n"]
    for p in all_papers:
        lines.append(f"**{p['title']}**")
        if p["authors"]:
            lines.append(f"  Authors: {', '.join(p['authors'][:5])}")
        if p["abstract"]:
            lines.append(f"  Abstract: {p['abstract']}...")
        lines.append(f"  ArXiv: {p['arxiv_id']}")
        lines.append(f"  URL: {p['url']}")
        lines.append("")

    return "\n".join(lines)


async def get_paper(paper_id: str) -> str:
    """Get a paper's metadata by ArXiv ID via HuggingFace API."""
    url = f"{HF_API}/papers/{paper_id}"
    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        try:
            resp = await client.get(url)
            if resp.status_code != 200:
                return f"Paper '{paper_id}' not found."
            return _format_hf_paper(resp.json())
        except Exception as e:
            return f"Error fetching paper: {e}"


def _format_hf_paper(data: dict) -> str:
    """Format a HuggingFace paper API response."""
    authors = [a.get("name", "") for a in data.get("authors", []) if not a.get("hidden")]
    pid = data.get("id", "")
    lines = [f"**{data.get('title', 'Untitled')}**"]
    if authors:
        lines.append(f"  Authors: {', '.join(authors)}")
    if data.get("summary"):
        lines.append(f"  Abstract: {data['summary']}")
    lines.append(f"  ArXiv: {pid}")
    lines.append(f"  URL: https://huggingface.co/papers/{pid}")
    lines.append(f"  PDF: https://arxiv.org/pdf/{pid}.pdf")
    lines.append(f"  Upvotes: {data.get('upvotes', 0)}")
    return "\n".join(lines)


async def read_paper_url(paper_url: str) -> str:
    """Extract and read text from a paper PDF or HTML URL."""
    try:
        resp = requests.get(paper_url, timeout=60, headers=HEADERS)
        if resp.headers.get("content-type", "").startswith("application/pdf"):
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(resp.content))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text if text.strip() else "Could not extract text from PDF."
        else:
            return resp.text[:50000]
    except Exception as e:
        return f"Error reading paper: {e}"
