"""
Smoke tests for all paper sources.

Each test verifies that a source module can be imported and its main
functions execute without crashing.  We use a simple "deep learning"
query so that every source is expected to return *something*.

These are integration tests that hit real APIs, so they are allowed
to be slow and may occasionally fail due to rate-limiting or network
issues.
"""

import importlib
import pytest

# ── helpers ──────────────────────────────────────────────────────────

QUERY = "deep learning"
MAX_RESULTS = 2

# Functional async source modules (original PaperCli)
ASYNC_SOURCE_MODULES = [
    "paper_cli.sources.arxiv",
    "paper_cli.sources.dblp",
    "paper_cli.sources.scholar",
    "paper_cli.sources.paperswithcode",
    "paper_cli.sources.huggingface",
    "paper_cli.sources.semanticscholar",
    "paper_cli.sources.crossref",
    "paper_cli.sources.openalex",
    "paper_cli.sources.pubmed",
    "paper_cli.sources.biorxiv",
    "paper_cli.sources.europepmc",
    "paper_cli.sources.hal",
    "paper_cli.sources.pmc",
    "paper_cli.sources.doaj",
    "paper_cli.sources.zenodo",
    "paper_cli.sources.openaire",
    "paper_cli.sources.inspirehep",
    "paper_cli.sources.chemrxiv",
]

# Class-based source modules
CLASS_SOURCE_MODULES = [
    "paper_cli.sources.google_scholar",
    "paper_cli.sources.iacr",
    "paper_cli.sources.citeseerx",
    "paper_cli.sources.ssrn",
    "paper_cli.sources.base_search",
    "paper_cli.sources.medrxiv",
    "paper_cli.sources.sci_hub",
]

ALL_SOURCE_MODULES = ASYNC_SOURCE_MODULES + CLASS_SOURCE_MODULES

# Infrastructure modules
INFRA_MODULES = [
    "paper_cli.paper",
    "paper_cli.config",
    "paper_cli.utils",
    "paper_cli.sources.base",
    "paper_cli.sources.oaipmh",
]


# ── import tests ─────────────────────────────────────────────────────

@pytest.mark.parametrize("module_path", ALL_SOURCE_MODULES + INFRA_MODULES)
def test_source_importable(module_path: str):
    """Every source module should import without errors."""
    mod = importlib.import_module(module_path)
    assert mod is not None


# ── search / main-function tests ─────────────────────────────────────

async def _call_search(module_path: str):
    """Call the primary search/list function of a source module."""
    mod = importlib.import_module(module_path)
    name = module_path.rsplit(".", 1)[-1]

    if name == "arxiv":
        return await mod.search_papers(QUERY, MAX_RESULTS)
    elif name == "huggingface":
        return await mod.get_daily_papers()
    elif name == "paperswithcode":
        return await mod.search_papers(title=QUERY)
    elif name == "chemrxiv":
        return await mod.search(QUERY, MAX_RESULTS)
    elif name in (
        "dblp", "scholar", "semanticscholar", "crossref",
        "openalex", "pubmed", "biorxiv", "europepmc",
        "hal", "pmc", "doaj", "zenodo", "openaire", "inspirehep",
    ):
        return await mod.search(QUERY, MAX_RESULTS)
    else:
        pytest.skip(f"No known search entry-point for {name}")


@pytest.mark.parametrize("module_path", ASYNC_SOURCE_MODULES)
async def test_source_search(module_path: str):
    """Each async source's search function should return a non-empty string."""
    result = await _call_search(module_path)
    assert isinstance(result, str)
    assert len(result) > 0


# ── unified search test ──────────────────────────────────────────────

async def test_unified_search():
    """The unified search tool should aggregate results."""
    from paper_cli.sources import unified

    result = await unified.search(QUERY, None, MAX_RESULTS)
    assert isinstance(result, str)
    assert "Unified Search" in result or "No results" in result
