FROM kalilinux/kali-rolling:latest

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/app

# Update and install only necessary tools
RUN echo "Starting Kali Linux IoT Scanner Build..." && \
    apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    curl \
    wget \
    git \
    sqlite3 \
    ffmpeg \
    net-tools \
    iputils-ping \
    tcpdump \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create application directory and user
RUN useradd -m -u 1000 iottester && \
    mkdir -p /app && chown iottester:iottester /app

WORKDIR /app

# Copy requirements first for better caching
COPY --chown=iottester:iottester requirements.txt .

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt

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

# Run verification tests on container start
CMD ["sh", "-c", "python3 verification_test.py && python3 server.py"]
