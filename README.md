# MD2PDF - Markdown to PDF Converter

Simply merge multiple markdown files to one PDF optimized for e-readers. A Streamlit web application that aggregates multiple Markdown files (like those downloaded from Perplexity AI) and converts them into a single, well-formatted PDF suitable for e-readers.

## Features

- 📁 Upload multiple `.md` files at once
- ⋮⋮ Checkbox-based file selection with up/down reordering
- ⚙️ Customizable PDF formatting options
- 🔗 Preserves original links and formatting
- 📱 E-reader friendly output
- 🐳 Docker support for easy deployment

## Quick Start

### Local Installation

1. **Create and activate virtual environment:**
   ```bash
   # Create virtual environment
   python3 -m venv venv
   
   # Activate virtual environment
   source venv/bin/activate  # On Linux/macOS
   # or
   venv\Scripts\activate     # On Windows
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install system dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install pandoc texlive-xetex texlive-fonts-recommended
   
   # macOS
   brew install pandoc
   # + Install MacTeX from https://tug.org/mactex/
   
   # Windows
   # Download Pandoc from https://pandoc.org
   # Download MiKTeX from https://miktex.org
   ```

4. **Run the application:**
   ```bash
   # Make sure venv is activated (you should see (venv) in your prompt)
   streamlit run app.py
   ```

5. **Open your browser** to `http://localhost:8501`

### Docker Usage

1. **Build and run:**
   ```bash
   docker build -t md2pdf .
   docker run -p 8501:8501 md2pdf
   ```

2. **Access the app** at `http://localhost:8501`

## How to Use

1. **Upload** your Markdown files from Perplexity AI or other sources
2. **Reorder** files by selecting them in your preferred sequence
3. **Customize** PDF options (font size, margins, code highlighting, etc.)
4. **Generate** and download your merged PDF

## PDF Customization Options

- Font sizes: 10pt to 14pt
- Margins: 1.5cm to 3cm
- Code highlighting styles: monochrome, kate, pygments, tango, zenburn
- Optional table of contents
- Clickable links preserved
- Custom metadata (title, author, date)

## Requirements

- Python ≥ 3.9
- Streamlit
- Pandoc
- XeLaTeX (via TeX Live or MiKTeX)

## Perfect for

- 📚 Research document compilation
- 📖 Creating e-reader friendly documents
- 🤖 Aggregating AI-generated content
- 📄 Academic paper collections
- 💼 Report consolidation

---
*Made with ❤️ using Streamlit and Pandoc*
