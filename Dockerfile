# Use official Python base image
FROM python:3.11-slim

# Set environment variables for fly.io
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies for Pandoc and LaTeX
RUN apt-get update && apt-get install -y \
    wget \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-latex-extra \
    texlive-fonts-extra \
    fonts-liberation \
    fonts-dejavu \
    fonts-lmodern \
    fonts-source-code-pro \
    fonts-source-sans-pro \
    fontconfig \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -fv

# Install additional LaTeX packages for Eisvogel template
RUN tlmgr update --self || true && \
    tlmgr install sourcesanspro sourcecodepro sourceserifpro lm-math || true

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code and assets
COPY app.py ./
COPY eisvogel.latex ./
COPY background5.png ./

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port used by Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Default command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.runOnSave=false", "--server.allowRunOnSave=false"]