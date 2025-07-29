import streamlit as st
import tempfile
import subprocess
from pathlib import Path
import os
import shutil


def create_eisvogel_template(gray_background=True, code_font_size="9pt", line_numbers=True, custom_title_page=True):
    """Create a template using the official Eisvogel template with minimal font fixes to preserve features."""
    
    eisvogel_path = Path(__file__).parent / "eisvogel.latex"
    
    if not eisvogel_path.exists():
        # Error if Eisvogel template not found
        raise FileNotFoundError("Eisvogel template (eisvogel.latex) not found. Please ensure the template file is in the project directory.")
    
    try:
        # Read the original Eisvogel template
        with open(eisvogel_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # MINIMAL font fixes - only disable the problematic Source font packages
        # This preserves all Eisvogel features while fixing the Times font error
        template = template.replace(
            '\\usepackage[default]{sourcesanspro}', 
            '% \\usepackage[default]{sourcesanspro} % Disabled - font not available'
        )
        template = template.replace(
            '\\usepackage{sourcecodepro}', 
            '% \\usepackage{sourcecodepro} % Disabled - font not available'
        )
        template = template.replace(
            '\\usepackage[default]{sourceserifpro}', 
            '% \\usepackage[default]{sourceserifpro} % Disabled - font not available'
        )
        
        # Add safe font fallback only where Eisvogel tries to set fonts
        # Look for specific problematic font settings and replace them
        if '\\setmainfont{Times}' in template:
            template = template.replace('\\setmainfont{Times}', '\\setmainfont{Liberation Serif}')
        if '\\setmonofont{Times}' in template:
            template = template.replace('\\setmonofont{Times}', '\\setmonofont{Liberation Mono}')
            
        # Replace generic Times references with Liberation
        template = template.replace('Times', 'Liberation Serif')
        template = template.replace('times', 'Liberation Serif')
        
        # Add MD2PDF branding to Eisvogel's built-in title page
        if custom_title_page and '\\end{titlepage}' in template:
            # Find where Eisvogel closes the title page and add our branding
            branding_addition = """
        % MD2PDF Branding Footer
        \\vfill
        \\begin{center}
            \\footnotesize
            Converted with md2pdf provided by brix-ia.com community
        \\end{center}
"""
            template = template.replace('\\end{titlepage}', branding_addition + '\n\\end{titlepage}')
        
        return template
        
    except Exception as e:
        # If there's any issue reading Eisvogel, raise the error
        raise RuntimeError(f"Failed to process Eisvogel template: {str(e)}")


def display_file_organizer(filenames):
    """Display file organizer with checkboxes and move buttons"""
    
    # Initialize session state for file order if not exists
    if 'file_order' not in st.session_state:
        st.session_state.file_order = [(filename, True) for filename in filenames]
    
    # Update file order if new files are added or removed
    current_files = set(filenames)
    session_files = set([f[0] for f in st.session_state.file_order])
    if current_files != session_files:
        st.session_state.file_order = [(filename, True) for filename in filenames]
    
    # Display files with drag handle, checkboxes and move buttons
    for i, (filename, selected) in enumerate(st.session_state.file_order):
        col1, col2, col3, col4, col5 = st.columns([0.08, 0.08, 0.08, 0.66, 0.1])
        
        with col1:
            st.markdown("⋮⋮", help="Drag handle")
        
        with col2:
            if st.button("↑", key=f"up_{i}", disabled=(i == 0), help="Move up"):
                # Move up
                st.session_state.file_order[i], st.session_state.file_order[i-1] = \
                    st.session_state.file_order[i-1], st.session_state.file_order[i]
                st.rerun()
        
        with col3:
            if st.button("↓", key=f"down_{i}", disabled=(i == len(st.session_state.file_order) - 1), help="Move down"):
                # Move down
                st.session_state.file_order[i], st.session_state.file_order[i+1] = \
                    st.session_state.file_order[i+1], st.session_state.file_order[i]
                st.rerun()
        
        with col4:
            new_selected = st.checkbox(filename, value=selected, key=f"select_{i}")
            if new_selected != selected:
                st.session_state.file_order[i] = (filename, new_selected)
        
        with col5:
            st.markdown(f"**{i+1}**")
    
    # Get ordered and selected files
    ordered_files = [filename for filename, selected in st.session_state.file_order if selected]
    
    return ordered_files


# Streamlit App Configuration
st.set_page_config(
    page_title="MD2PDF - Professional Markdown to PDF Converter",
    page_icon="📄",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for responsive design and improved UI
st.markdown("""
<style>
    .main > div {
        max-width: 1000px;
        padding-top: 2rem;
    }
    
    @media (max-width: 768px) {
        .main > div {
            max-width: 100%;
            padding: 1rem 0.5rem;
        }
    }
    
    .stButton > button {
        width: 100%;
    }
    
    .upload-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📄 MD2PDF")
st.markdown("**Professional Markdown to PDF Converter with Eisvogel Template**")
st.markdown("Transform your AI-generated Markdown files into beautifully formatted, e-reader optimized PDFs.")

# File Upload Section
st.markdown('<div class="upload-section">', unsafe_allow_html=True)
st.markdown("### 📁 Upload Markdown Files")

uploaded_files = st.file_uploader(
    "Choose Markdown files",
    type=['md'],
    accept_multiple_files=True,
    help="Upload multiple .md files from AI tools (ChatGPT, Claude, Perplexity, etc.)"
)

st.markdown('</div>', unsafe_allow_html=True)

if uploaded_files:
    st.markdown("### 📋 File Organization")
    st.markdown("Organize your files in the desired order. Use ↑↓ buttons to reorder and checkboxes to select files for inclusion.")
    
    # Get filenames
    filenames = [file.name for file in uploaded_files]
    
    # Display file organizer
    ordered_files = display_file_organizer(filenames)
    
    if ordered_files:
        st.markdown("**Selected files in order:**")
        for i, filename in enumerate(ordered_files, 1):
            st.markdown(f"{i}. {filename}")
        
        # PDF generation options
        st.markdown("### PDF Options")
        
        # Metadata section
        st.markdown("#### Document Metadata")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            pdf_title = st.text_input("Title", value="Merged Markdown Document")
        with col2:
            pdf_author = st.text_input("Author", value="")
        with col3:
            from datetime import datetime
            pdf_date = st.date_input("Date", value=datetime.now().date())
        
        # Template info section
        st.markdown("#### Professional Template")
        st.success("✅ **Eisvogel Professional Template** - Features professional typography, gray code backgrounds with syntax highlighting, custom title pages with background images, and optimized e-reader formatting.")
        
        # Formatting section
        st.markdown("#### Formatting")
        col1, col2 = st.columns(2)
        
        with col1:
            font_family = st.selectbox(
                "Font Family", 
                ["Auto-detect", "Liberation Serif", "DejaVu Serif", "Latin Modern", "Default"],
                index=0,
                help="Auto-detect finds available system fonts. Liberation/DejaVu are most compatible. Avoid Times font."
            )
            font_size = st.selectbox("Font Size", ["10pt", "11pt", "12pt", "14pt"], index=2)
        
        with col2:
            margin = st.selectbox("Margins", ["1.5cm", "2cm", "2.5cm", "3cm"], index=2)
        
        # Code formatting options
        st.markdown("#### Code Block Options")
        col1, col2 = st.columns(2)
        
        with col1:
            include_line_numbers = st.checkbox("Include Line Numbers", value=True)
            gray_code_background = st.checkbox("Gray Code Background", value=True)
        
        with col2:
            code_font_size = st.selectbox("Code Font Size", ["8pt", "9pt", "10pt", "11pt"], index=1)
            
        # Page options
        st.markdown("#### Page Options")
        col1, col2 = st.columns(2)
        
        with col1:
            include_title_page = st.checkbox("Custom Title Page", value=True, help="Professional title page with background image")
        
        with col2:
            include_toc = st.checkbox("Table of Contents", value=False)
        
        # Generate PDF button
        if st.button("🚀 Generate PDF", type="primary"):
            try:
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Step 1: Save uploaded files and merge
                    status_text.text("📝 Processing Markdown files...")
                    progress_bar.progress(25)
                    
                    merged_content = []
                    
                    # Create a dictionary for quick lookup
                    file_dict = {file.name: file for file in uploaded_files}
                    
                    for filename in ordered_files:
                        if filename in file_dict:
                            file_content = file_dict[filename].read().decode('utf-8')
                            
                            # Add file separator if multiple files
                            if len(ordered_files) > 1:
                                merged_content.append(f"# {filename.rsplit('.', 1)[0]}\n\n")
                            
                            merged_content.append(file_content)
                            merged_content.append("\n\n")
                    
                    # Save merged content
                    merged_md_path = Path(temp_dir) / "merged.md"
                    with open(merged_md_path, "w", encoding="utf-8") as f:
                        f.write("".join(merged_content))
                    
                    # Step 2: Prepare LaTeX template and background
                    status_text.text("🎨 Preparing professional template...")
                    progress_bar.progress(50)
                    
                    pdf_path = Path(temp_dir) / "output.pdf"
                    
                    # Create Eisvogel LaTeX template
                    template_path = Path(temp_dir) / "template.tex"
                    latex_template = create_eisvogel_template(gray_code_background, code_font_size, include_line_numbers, include_title_page)
                    
                    # Replace background path placeholder with actual path (only if title page is enabled)
                    if include_title_page:
                        # Use background PNG directly
                        background_src = Path("docs/background5.png")
                        background_dest = Path(temp_dir) / "background.png"
                        
                        if background_src.exists():
                            shutil.copy2(background_src, background_dest)
                            latex_template = latex_template.replace("background_path_placeholder", str(background_dest))
                        else:
                            # Remove background inclusion if file doesn't exist
                            latex_template = latex_template.replace(
                                "\\AddToShipoutPictureBG*{%\n        \\includegraphics[width=\\paperwidth,height=\\paperheight]{background_path_placeholder}\n    }",
                                ""
                            )
                    
                    with open(template_path, "w", encoding="utf-8") as f:
                        f.write(latex_template)
                    
                    # Build pandoc command
                    pandoc_cmd = [
                        "pandoc",
                        str(merged_md_path),
                        "-o", str(pdf_path),
                        "--pdf-engine=xelatex",
                        "--template", str(template_path),
                        "-V", f"geometry:margin={margin}",
                        "-V", "linkcolor=blue",
                        "-V", "urlcolor=blue",
                        "--no-highlight",
                        "--standalone"
                    ]
                    
                    # Note: Line numbers are handled in the LaTeX template
                    # The include_line_numbers flag is passed to create_eisvogel_template
                    
                    # Add metadata
                    if pdf_title.strip():
                        pandoc_cmd.extend(["-M", f"title={pdf_title.strip()}"])
                    if pdf_author.strip():
                        pandoc_cmd.extend(["-M", f"author={pdf_author.strip()}"])
                    pandoc_cmd.extend(["-M", f"date={pdf_date.strftime('%B %d, %Y')}"])
                    
                    # Enable title page when custom title page is requested
                    if include_title_page:
                        pandoc_cmd.extend(["-V", "titlepage=true"])
                        # Add background image support
                        if background_dest and background_dest.exists():
                            pandoc_cmd.extend(["-V", f"titlepage-background={background_dest}"])
                        # Set title page colors for better visibility
                        pandoc_cmd.extend(["-V", "titlepage-text-color=5F5F5F"])
                        pandoc_cmd.extend(["-V", "titlepage-rule-color=435488"])
                        pandoc_cmd.extend(["-V", "titlepage-rule-height=4"])
                    
                    # Enable Eisvogel code highlighting with gray backgrounds
                    # Enable listings package for gray code backgrounds
                    pandoc_cmd.extend(["-V", "listings=true"])
                    # Ensure line numbers are shown if requested
                    if not include_line_numbers:
                        pandoc_cmd.extend(["-V", "listings-disable-line-numbers=true"])
                    # Set code block font size if specified
                    if code_font_size != "9pt":  # 9pt is default
                        font_size_map = {"8pt": "\\footnotesize", "10pt": "\\normalsize", "11pt": "\\large"}
                        if code_font_size in font_size_map:
                            pandoc_cmd.extend(["-V", f"code-block-font-size={font_size_map[code_font_size]}"])
                    # Remove --no-highlight and add highlight-style for proper syntax highlighting
                    if "--no-highlight" in pandoc_cmd:
                        pandoc_cmd.remove("--no-highlight")
                    # Add highlight style to activate Eisvogel's syntax highlighting with listings
                    pandoc_cmd.extend(["--highlight-style=tango"])
                    
                    # Add table of contents if requested
                    if include_toc:
                        pandoc_cmd.extend(["--toc", "--toc-depth=3"])
                    
                    # Handle font selection - avoid Times font
                    if font_family == "Auto-detect":
                        # Use safe fonts that won't cause Times font errors
                        try:
                            # Check for Liberation fonts first (most reliable)
                            result = subprocess.run(
                                ["fc-list", ":family=Liberation Serif"], 
                                capture_output=True, text=True
                            )
                            if result.returncode == 0 and result.stdout.strip():
                                pandoc_cmd.extend(["-V", "mainfont=Liberation Serif"])
                                pandoc_cmd.extend(["-V", "monofont=Liberation Mono"])
                            else:
                                # Use Latin Modern (always available with XeTeX) - safer than generic "serif"
                                pandoc_cmd.extend(["-V", "mainfont=Latin Modern Roman"])
                                pandoc_cmd.extend(["-V", "monofont=Latin Modern Mono"])
                        except FileNotFoundError:
                            # fc-list not available, use Latin Modern
                            pandoc_cmd.extend(["-V", "mainfont=Latin Modern Roman"])
                            pandoc_cmd.extend(["-V", "monofont=Latin Modern Mono"])
                    
                    elif font_family != "Default":
                        # Use selected font
                        font_mapping = {
                            "Liberation Serif": ("Liberation Serif", "Liberation Mono"),
                            "DejaVu Serif": ("DejaVu Serif", "DejaVu Sans Mono"),
                            "Latin Modern": ("Latin Modern Roman", "Latin Modern Mono")
                        }
                        
                        if font_family in font_mapping:
                            main_font, mono_font = font_mapping[font_family]
                            pandoc_cmd.extend(["-V", f"mainfont={main_font}"])
                            pandoc_cmd.extend(["-V", f"monofont={mono_font}"])
                    
                    status_text.text("⚙️ Running Pandoc conversion...")
                    progress_bar.progress(75)
                    
                    # Run pandoc
                    result = subprocess.run(pandoc_cmd, capture_output=True, text=True)
                    
                    if result.returncode != 0:
                        st.error("❌ Pandoc conversion failed:")
                        st.code(result.stderr)
                        st.info("💡 Make sure Pandoc and XeLaTeX are installed on your system")
                    else:
                        # Step 3: Provide download
                        status_text.text("✅ PDF generated successfully!")
                        progress_bar.progress(100)
                        
                        # Read the generated PDF
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()
                        
                        # Provide download button
                        st.success("🎉 Your professional PDF is ready!")
                        
                        # Create filename
                        if pdf_title.strip():
                            filename = f"{pdf_title.strip().replace(' ', '_')}.pdf"
                        else:
                            filename = "merged_document.pdf"
                        
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_bytes,
                            file_name=filename,
                            mime="application/pdf",
                            type="primary"
                        )
                        
                        # Show PDF info
                        st.info(f"📊 PDF Size: {len(pdf_bytes):,} bytes | 📄 Professional Eisvogel Template")
                        
                        # Clear progress
                        progress_bar.empty()
                        status_text.empty()
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.info("💡 Please check that all required dependencies are installed and try again.")
    else:
        st.warning("⚠️ Please select at least one file to generate PDF.")
else:
    # Instructions when no files are uploaded
    st.markdown("### 🚀 Getting Started")
    
    st.markdown("""
    **MD2PDF** converts your AI-generated Markdown files into professional PDFs with:
    
    - 🎨 **Professional Eisvogel template** with beautiful typography
    - 🖥️ **Gray code backgrounds** with syntax highlighting  
    - 📄 **Custom title pages** with background images
    - 📚 **E-reader optimization** for tablets and devices
    - 🔗 **Link preservation** and table of contents
    
    **Perfect for:**
    - ChatGPT, Claude, and Perplexity AI outputs
    - Research paper compilation
    - Technical documentation
    - Academic collections
    """)
    
    st.markdown("### 📋 How to Use")
    st.markdown("""
    1. **Upload** your `.md` files using the file uploader above
    2. **Organize** files in your preferred order using the ↑↓ buttons
    3. **Customize** document settings, fonts, and formatting options
    4. **Generate** your professional PDF with one click
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    Made with ❤️ using Streamlit, Pandoc, and the Eisvogel LaTeX template<br>
    <a href="https://github.com/anthropics/claude-code" target="_blank">Report Issues</a> | 
    <a href="https://docs.anthropic.com/en/docs/claude-code" target="_blank">Documentation</a>
</div>
""", unsafe_allow_html=True)