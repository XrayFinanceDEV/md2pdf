# Use official Python base image
FROM python:3.11-slim

# Install dependencies for Pandoc and LaTeX
RUN apt-get update && apt-get install -y \
    wget \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-latex-extra \
    fonts-liberation \
    fontconfig \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY app.py ./

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port used by Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Default command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]