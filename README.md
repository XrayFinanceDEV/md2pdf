## 🚀 MD2PDF - Professional Markdown to PDF Converter

Convert AI-generated Markdown files into beautifully formatted, e-reader optimized PDFs with professional styling options.

## ✨ Key Features

- 📁 **Multi-file Upload**: Process multiple `.md` files simultaneously
- ⋮⋮ **Smart Reordering**: Drag-and-drop file organization with checkboxes
- 🎨 **Professional Template**: Eisvogel LaTeX template with optimal styling
- 🖥️ **Enhanced Code Blocks**: Gray backgrounds, syntax highlighting, line numbers
- 📄 **Custom Title Pages**: Professional backgrounds with branding
- 🔗 **Link Preservation**: Maintains clickable links and formatting
- 📱 **E-reader Optimized**: Perfect for tablets and e-ink devices
- 🐳 **Flexible Deployment**: Streamlit Cloud or Docker with full LaTeX support

## 🎯 Professional Template

**Eisvogel LaTeX Template** - The gold standard for professional document generation:
- ✅ **Beautiful typography** with optimal font selection and spacing
- ✅ **Gray code backgrounds** with syntax highlighting in multiple languages  
- ✅ **Professional title pages** with background image support
- ✅ **Advanced formatting** including tables, lists, and mathematical expressions
- ✅ **E-reader optimization** for tablets and mobile devices
- ✅ **Reliable font handling** with automatic fallbacks
- ✅ **ASCII art preservation** with proper monospace formatting

## 🌐 Live Demo

**Streamlit Cloud**: https://md2pdf-brixia.streamlit.app/
- Professional Eisvogel template with all features
- Perfect for quick conversions and testing

## 🚀 Deployment Options

### Option 1: Local Development

1. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or venv\Scripts\activate  # Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   
   # System dependencies (Ubuntu/Debian)
   sudo apt-get install pandoc texlive-xetex texlive-fonts-recommended
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   # Visit http://localhost:8501
   ```

### Option 2: Docker (Local)

**Quick Start:**
```bash
docker build -t md2pdf .
docker run -p 8501:8501 md2pdf
# Visit http://localhost:8501
```

**Features**: Full Eisvogel template support with all LaTeX packages

### Option 3: Fly.io Production Deployment 🏆

**Best for production use with full LaTeX support.**

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Deploy:**
   ```bash
   flyctl auth login
   flyctl launch
   ```

3. **Features:**
   - ✅ Professional Eisvogel template fully supported
   - ✅ Auto-scaling (0-1 machines)
   - ✅ Built-in monitoring
   - ✅ HTTPS by default
   - ✅ ~$5-20/month depending on usage

📖 **See `FLY_DEPLOYMENT.md` for complete fly.io setup guide**

### Option 4: Streamlit Cloud

- ✅ Professional Eisvogel template with font compatibility fixes
- ✅ All features including gray code backgrounds and title pages
- ✅ Free hosting option for personal use

## 📋 How to Use

1. **Upload Files**: Add your `.md` files from AI tools (Perplexity, ChatGPT, Claude, etc.)
2. **Organize Content**: Reorder files using checkboxes in your preferred sequence  
3. **Customize Format**: 
   - Set document metadata (title, author, date)
   - Choose fonts, sizes, and margins
   - Configure code block styling and line numbers
   - Enable/disable professional title page and table of contents
4. **Generate PDF**: Click "Generate PDF" and download your professional Eisvogel-styled document

## ⚙️ Customization Options

### Document Settings
- **Professional Template**: Eisvogel LaTeX template with advanced typography
- **Smart Fonts**: Auto-detect system fonts with Liberation/Latin Modern fallbacks
- **Font Sizes**: 10pt to 14pt document font sizes
- **Page Margins**: 1.5cm to 3cm customizable margins

### Code Block Features
- **Gray backgrounds** (RGB 247,247,247) with professional borders
- **Syntax highlighting** for JavaScript, Python, SQL, and 100+ languages
- **Line numbers** for better code readability
- **Configurable font sizes** (8pt to 11pt) for code blocks
- **ASCII art preservation** with proper monospace formatting

### Professional Features
- **Custom title pages** with background images and professional styling
- **Table of contents** generation with configurable depth
- **Clickable links** and cross-references preserved from Markdown
- **E-reader optimization** for tablets and e-ink devices
- **Document metadata** (title, author, date) with LaTeX formatting

## 🎯 Perfect For

- 📚 **Research Compilation**: Merge multiple research papers and articles
- 🤖 **AI Content Aggregation**: Convert ChatGPT, Claude, Perplexity outputs  
- 📖 **E-reader Documents**: Tablet and e-ink device optimization
- 📄 **Academic Collections**: Course materials and paper compilation
- 💼 **Professional Reports**: Business document consolidation
- 📓 **Documentation**: Technical guides and manuals

## 🔧 Technical Requirements

- **Python**: ≥ 3.9
- **Core**: Streamlit, Pandoc, XeLaTeX
- **Fonts**: Liberation fonts (included), Source fonts (Docker)
- **LaTeX**: texlive-xetex, texlive-fonts-recommended

## 🆘 Troubleshooting

### Template Issues
- **Font compatibility**: App auto-detects and uses Liberation/Latin Modern fonts
- **Docker deployment**: Provides full LaTeX package support for maximum compatibility
- **Streamlit Cloud**: Works with built-in font compatibility fixes

### System Issues
- **Pandoc not found**: Install from [pandoc.org](https://pandoc.org)
- **LaTeX errors**: Install XeLaTeX via TeX Live or MiKTeX  
- **Font issues**: App auto-detects and falls back to system fonts
- **Background missing**: Ensure `docs/background5.png` exists

### Fixed Issues ✅
- **FancyVerb errors**: Resolved with improved LaTeX template handling
- **Gray code backgrounds**: Now working perfectly with Eisvogel template
- **Font compatibility**: Automatic Liberation font fallbacks implemented
- **Title page rendering**: Professional cover pages with background images working
- **ASCII art preservation**: Monospace formatting maintains box-drawing characters

## 🌟 Recent Updates

- ✅ **Simplified to Eisvogel Only**: Clean interface with one professional template
- ✅ **Perfect Code Formatting**: Gray backgrounds + syntax highlighting working
- ✅ **Font Compatibility**: Auto-detection with Liberation font fallbacks
- ✅ **Title Page Fix**: Professional cover pages with background images
- ✅ **ASCII Art Support**: Proper monospace formatting for diagrams
- ✅ **Enhanced Reliability**: Robust error handling and deployment options

---
*Made with ❤️ using Streamlit, Pandoc, and the Eisvogel LaTeX template*

**Contributing**: Issues and PRs welcome on GitHub  
**License**: Open source - see license file for details
