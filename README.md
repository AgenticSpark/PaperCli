# PaperCli — All-in-One Academic Paper Search CLI

A single command-line tool to **search, download, and read** academic papers
across **25+ keyless sources** — ArXiv, PubMed, Semantic Scholar, CrossRef,
OpenAlex, Google Scholar, DBLP, and many more. **No API keys, no accounts, no auth.**

## Supported Sources

All sources are free and require **no authentication**.

| # | Source | Type |
|---|--------|------|
| 1 | **ArXiv** | Preprints (CS, Physics, Math) |
| 2 | **PubMed** | Biomedical literature |
| 3 | **Semantic Scholar** | AI-powered academic search |
| 4 | **CrossRef** | DOI metadata |
| 5 | **OpenAlex** | Open scholarly metadata |
| 6 | **DBLP** | Computer science bibliography |
| 7 | **Google Scholar** | Web scraping (scholarly lib) |
| 8 | **Google Scholar (HTML)** | Direct HTML parsing |
| 9 | **bioRxiv** | Biology preprints |
| 10 | **medRxiv** | Medical preprints |
| 11 | **Europe PMC** | European biomedical literature |
| 12 | **PubMed Central** | Full-text biomedical articles |
| 13 | **HuggingFace** | Daily trending AI papers |
| 14 | **PapersWithCode** | ML papers with code |
| 15 | **HAL** | French national open archive |
| 16 | **DOAJ** | Open access journals |
| 17 | **Zenodo** | Open research data |
| 18 | **OpenAIRE** | European open access |
| 19 | **INSPIRE-HEP** | High energy physics |
| 20 | **Unpaywall** | Open access DOI resolver |
| 21 | **IACR** | Cryptography ePrint archive |
| 22 | **CiteSeerX** | CS digital library |
| 23 | **SSRN** | Social science preprints |
| 24 | **BASE** | Bielefeld Academic Search Engine |
| 25 | **ChemRxiv** | Chemistry preprints |
| 26 | **Sci-Hub** | PDF fetcher |

## Quick Start

### Install
```bash
pip install -e .
# or
uv pip install -e .
```

This installs two equivalent commands: `paper-cli` and `paper-search`.

### Usage
```bash
# Search across all sources
paper-cli search "transformer architectures" -n 5

# Search specific sources
paper-cli search "CRISPR" -s pubmed,biorxiv,europepmc

# Download a paper PDF
paper-cli download arxiv 2401.12345

# Read paper text (download + extract)
paper-cli read arxiv 2401.12345

# List available sources
paper-cli sources
```

You can also run it as a module:
```bash
python -m paper_cli search "diffusion models" -n 3
```

## Commands

### `search <query> [-n N] [-s SOURCES]`
Search for papers across sources in parallel and print merged results.
- `-n, --max-results`: results per source (default: 5)
- `-s, --sources`: comma-separated sources or `all` (default: all)

### `download <source> <paper_id> [-o DIR]`
Download a paper PDF. `-o` sets the output directory (default: `./downloads`).

### `read <source> <paper_id> [-o DIR]`
Download and extract the full text of a paper.

### `sources`
List every available source.

## Source Aliases

| Alias | Source |
|-------|--------|
| `arxiv` | ArXiv |
| `ss`, `s2`, `semanticscholar` | Semantic Scholar |
| `scholar`, `google` | Google Scholar (scholarly) |
| `google_scholar` | Google Scholar (HTML) |
| `crossref`, `cr` | CrossRef |
| `openalex`, `oa` | OpenAlex |
| `pubmed`, `pm` | PubMed |
| `pmc`, `pubmedcentral` | PubMed Central |
| `biorxiv` | bioRxiv |
| `medrxiv` | medRxiv |
| `europepmc`, `epmc` | Europe PMC |
| `hf`, `huggingface` | HuggingFace |
| `pwc`, `paperswithcode` | PapersWithCode |
| `dblp` | DBLP |
| `hal` | HAL |
| `doaj` | DOAJ |
| `zenodo` | Zenodo |
| `openaire` | OpenAIRE |
| `inspirehep`, `inspire` | INSPIRE-HEP |
| `iacr` | IACR ePrint |
| `citeseerx` | CiteSeerX |
| `ssrn` | SSRN |
| `base` | BASE |
| `chemrxiv` | ChemRxiv |
| `unpaywall` | Unpaywall |

## Configuration

PaperCli works out of the box with **no configuration**. The only optional
environment variables are conveniences (not credentials):

```bash
# Storage path for downloaded papers (default: ~/.paper-cli/papers)
PAPER_CLI_STORAGE=~/.paper-cli/papers

# Optional proxy for Google Scholar to avoid rate limits
PAPER_CLI_GOOGLE_SCHOLAR_PROXY_URL=
```

## Docker

```bash
docker build -t paper-cli .
docker run --rm paper-cli search "graph neural networks" -n 3
```

## Project Structure

```
src/paper_cli/
├── __init__.py          # Package entry point
├── __main__.py          # python -m paper_cli
├── cli.py               # CLI interface (paper-cli / paper-search)
├── paper.py             # Paper dataclass model
├── config.py            # Environment configuration
├── utils.py             # DOI extraction utilities
└── sources/
    ├── unified.py       # Parallel search dispatcher
    ├── base.py          # Abstract PaperSource base class
    ├── oaipmh.py        # OAI-PMH protocol base
    ├── arxiv.py         # ArXiv
    ├── pubmed.py        # PubMed
    ├── semanticscholar.py # Semantic Scholar
    ├── crossref.py      # CrossRef
    ├── openalex.py      # OpenAlex
    ├── dblp.py          # DBLP
    ├── scholar.py       # Google Scholar (scholarly)
    ├── google_scholar.py # Google Scholar (HTML)
    ├── biorxiv.py       # bioRxiv
    ├── medrxiv.py       # medRxiv
    ├── europepmc.py     # Europe PMC
    ├── pmc.py           # PubMed Central
    ├── huggingface.py   # HuggingFace Daily Papers
    ├── paperswithcode.py # PapersWithCode
    ├── openreview.py    # OpenReview
    ├── hal.py           # HAL
    ├── doaj.py          # DOAJ
    ├── zenodo.py        # Zenodo
    ├── openaire.py      # OpenAIRE
    ├── inspirehep.py    # INSPIRE-HEP
    ├── unpaywall.py     # Unpaywall
    ├── iacr.py          # IACR ePrint
    ├── citeseerx.py     # CiteSeerX
    ├── ssrn.py          # SSRN
    ├── base_search.py   # BASE
    ├── chemrxiv.py      # ChemRxiv
    └── sci_hub.py       # Sci-Hub
```

## License

MIT
