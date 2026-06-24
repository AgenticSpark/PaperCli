# Multi-stage build for smaller image
FROM python:3.12-slim AS builder

WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src/ src/

RUN pip install --no-cache-dir build \
    && python -m build --wheel \
    && pip install --no-cache-dir dist/*.whl

FROM python:3.12-slim

WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/paper-cli /usr/local/bin/paper-cli
COPY --from=builder /usr/local/bin/paper-search /usr/local/bin/paper-search

# Optional (non-credential) settings — override at runtime with -e
ENV PAPER_CLI_STORAGE=""
ENV PAPER_CLI_GOOGLE_SCHOLAR_PROXY_URL=""

ENTRYPOINT ["paper-cli"]
CMD ["sources"]
