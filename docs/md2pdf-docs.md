# Technical Documentation

## Python Project: Merge and Convert Markdown Files (.md) via Streamlit Web App

### Project Overview

Create a web application using Python and Streamlit that enables users to:

- Upload single or multiple Markdown files (.md) exported from Perplexity or other AI tools
- Manually select and reorder the Markdown files
- Merge the ordered Markdown contents into a single file
- Convert the merged Markdown file into a well-formatted PDF using Pandoc
- Download the generated PDF directly from the web interface


## Technical Requirements

- Python ≥ 3.9
- Streamlit (`pip install streamlit`)
- [Pandoc](https://pandoc.org/) installed on the host machine
- LaTeX engine (e.g., XeLaTeX via MiKTeX or TeX Live) installed for PDF generation
- Python libraries: `streamlit`
- Access to run subprocess commands from Python (to call Pandoc)


## Functional Specification

### 1. Upload Multiple Markdown Files

- Use Streamlit’s `st.file_uploader` with `accept_multiple_files=True` and file type filter on `.md`
- Display list of uploaded files


### 2. File Selection and Ordering

- Provide an interface to select and reorder the uploaded Markdown files (using a reorderable multi-select widget or buttons to move files up/down)
- Show filenames and optionally preview small snippets


### 3. Merge Markdown Files

- Upon user confirmation, concatenate the Markdown files in the selected order into a temporary `.md` file on disk


### 4. Convert Markdown to PDF

- Call `pandoc` via Python’s `subprocess` module to convert the merged markdown file to PDF
- Use `xelatex` as PDF engine for better font support
- Pass options for font (`Calibri` or `Open Sans`), code highlighting style, margins, font sizes, etc.


### 5. PDF Download

- Provide a Streamlit download button to download the generated PDF
- Handle temporary files and clean up after download


## Example Python Code Snippet (Streamlit App)

```python
import streamlit as st
import tempfile
import subprocess
from pathlib import Path

st.title("Markdown Merger & PDF Converter")

# Step 1: Upload Markdown Files
md_files = st.file_uploader("Upload one or more Markdown (.md) files:", type='md', accept_multiple_files=True)

if md_files:
    filenames = [file.name for file in md_files]

    # Step 2: Select and order files (simple multi-select for ordering)
    order = st.multiselect(
        "Select and order files (drag to reorder):",
        options=filenames,
        default=filenames
    )

    if st.button("Generate PDF"):
        with tempfile.TemporaryDirectory() as temp_dir:
            merged_md_path = Path(temp_dir) / "merged.md"
            with open(merged_md_path, "w", encoding="utf-8") as outfile:
                for fname in order:
                    # find the file object by name
                    uploaded_file = next(f for f in md_files if f.name == fname)
                    content = uploaded_file.read().decode("utf-8")
                    outfile.write(content + "\n\n")

            pdf_path = Path(temp_dir) / "output.pdf"
            # Pandoc command with formatting options
            pandoc_cmd = [
                "pandoc",
                str(merged_md_path),
                "-o",
                str(pdf_path),
                "--pdf-engine=xelatex",
                "-V", "mainfont=Calibri",
                "-V", "monofont=Fira Mono",
                "-V", "fontsize=12pt",
                "-V", "geometry:margin=2.5cm",
                "--highlight-style=espresso"
            ]

            try:
                subprocess.run(pandoc_cmd, check=True)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="Download PDF",
                        data=pdf_file,
                        file_name="merged_document.pdf",
                        mime="application/pdf"
                    )
            except subprocess.CalledProcessError:
                st.error("Error: Failed to generate PDF. Please make sure Pandoc and LaTeX are installed properly.")
```


## Best Practices

- Use [Pandoc Eisvogel template](https://github.com/Wandmalfarbe/pandoc-latex-template) for professional PDF layouts
- Handle encoding and special characters properly
- Provide user feedback and error handling (e.g., unsupported characters, file read errors)
- Optionally support EPUB creation for Kindle friendly output
- Add preview functionality to check Markdown content before conversion


## Docker Deployment

### Dockerizing the Streamlit App with Pandoc and LaTeX

To deploy the app in a containerized environment, you need to create a Docker image that includes:

- Python environment with Streamlit and dependencies
- Pandoc installed
- LaTeX engine installed (e.g., TeX Live or TinyTeX) for PDF compilation


### Dockerfile Example

```dockerfile
# Use official Python base image
FROM python:3.10-slim

# Install dependencies for Pandoc and LaTeX
RUN apt-get update && apt-get install -y \
    wget \
    pandoc \
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-recommended \
    texlive-latex-extra \
    fonts-liberation \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements (if any)
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port used by Streamlit
EXPOSE 8501

# Default command to run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```


### requirements.txt Example

```
streamlit
```


### Build and Run Container

```bash
# Build the Docker image
docker build -t md-pdf-streamlit-app .

# Run the container and publish port 8501
docker run -d -p 8501:8501 md-pdf-streamlit-app
```


## Notes for Deployment

- The Docker container includes Pandoc and XeLaTeX as required for PDF generation
- Ensure enough disk and memory resources for LaTeX processing
- You can customize the Dockerfile to add fonts like Calibri or Open Sans if licensing allows, or use preinstalled free fonts
- For cloud deployment: check if your provider allows sufficient container permissions and resource limits for LaTeX builds


# Summary

This documentation covers:

- A Python + Streamlit app for Markdown upload, merge, and PDF conversion
- Usage of Pandoc with XeLaTeX for PDF formatting from Markdown
- A Docker-based deployment approach for easy hosting with all dependencies bundled

This setup enables flexible handling of AI-exported Markdown files and converting them to reading-friendly PDF (or potential ePub) formats accessible directly in a browser.

If you want, I can provide you with a fully working GitHub repo example with this code and Dockerfile!

