FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    nmap \
    curl \
    wget \
    sqlite3 \
    net-tools \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create application directory and user
RUN useradd -m -u 1000 iottester && \
    mkdir -p /app && chown iottester:iottester /app

WORKDIR /app

# Copy requirements first for better caching
COPY --chown=iottester:iottester requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY --chown=iottester:iottester server.py .
COPY --chown=iottester:iottester iot_signatures.json .
COPY --chown=iottester:iottester legal_warning.md .
COPY --chown=iottester:iottester verification_test.py .
COPY --chown=iottester:iottester mcp_compliance_test.py .

# Initialize database
RUN sqlite3 camera_vulnerabilities.db "CREATE TABLE IF NOT EXISTS scan_results ( \
    id INTEGER PRIMARY KEY AUTOINCREMENT, \
    target TEXT NOT NULL, \
    scan_type TEXT NOT NULL, \
    vulnerabilities_found TEXT, \
    severity TEXT, \
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP \
)" && chown iottester:iottester camera_vulnerabilities.db

USER iottester

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python3 -c "import sys; sys.exit(0)"

# Run the server
CMD ["python3", "server.py"]
