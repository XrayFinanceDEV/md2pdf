import streamlit as st
import tempfile
import subprocess
from pathlib import Path
import os

st.set_page_config(
    page_title="MD2PDF - Markdown to PDF Converter",
    page_icon="📄",
    layout="wide"
)

st.title("📄 MD2PDF - Markdown to PDF Converter")
st.markdown("Convert and merge your Perplexity AI and other Markdown files into a single PDF for e-readers")

st.markdown("### Upload Markdown Files")
md_files = st.file_uploader(
    "Upload one or more Markdown (.md) files:",
    type=['md'],
    accept_multiple_files=True,
    help="Select multiple .md files exported from Perplexity AI or other sources"
)

if md_files:
    st.success(f"✅ {len(md_files)} file(s) uploaded successfully")
    
    filenames = [file.name for file in md_files]
    
    # File ordering interface
    st.markdown("### Select and Order Files")
    st.info("💡 Use ⋮⋮ buttons to reorder, checkboxes to select files")
    
    # Initialize session state for file order if not exists
    if 'file_order' not in st.session_state:
        st.session_state.file_order = [(filename, True) for filename in filenames]
    
    # Update session state if files have changed
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
        
        # Formatting section
        st.markdown("#### Formatting")
        col1, col2 = st.columns(2)
        
        with col1:
            font_family = st.selectbox(
                "Font Family", 
                ["Auto-detect", "Open Sans", "Liberation Serif", "DejaVu Serif", "Times", "Default"],
                index=0
            )
            font_size = st.selectbox("Font Size", ["10pt", "11pt", "12pt", "14pt"], index=2)
        
        with col2:
            margin = st.selectbox("Margins", ["1.5cm", "2cm", "2.5cm", "3cm"], index=2)
            highlight_style = st.selectbox(
                "Code Highlight Style",
                ["monochrome", "kate", "pygments", "tango", "zenburn"],
                index=0
            )
        
        include_toc = st.checkbox("Include Table of Contents", value=True)
        
        # Generate PDF button
        if st.button("🔄 Generate PDF", type="primary"):
            if not ordered_files:
                st.error("Please select at least one file to convert")
            else:
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    with tempfile.TemporaryDirectory() as temp_dir:
                        # Step 1: Merge files
                        status_text.text("📝 Merging Markdown files...")
                        progress_bar.progress(25)
                        
                        merged_md_path = Path(temp_dir) / "merged.md"
                        
                        with open(merged_md_path, "w", encoding="utf-8") as outfile:
                            for i, fname in enumerate(ordered_files):
                                uploaded_file = next(f for f in md_files if f.name == fname)
                                
                                # Reset file pointer
                                uploaded_file.seek(0)
                                content = uploaded_file.read().decode("utf-8")
                                
                                # Add file separator with title
                                if i > 0:
                                    outfile.write("\n\n---\n\n")
                                
                                outfile.write(f"# {fname.replace('.md', '')}\n\n")
                                outfile.write(content)
                                outfile.write("\n\n")
                        
                        # Step 2: Convert to PDF
                        status_text.text("🔄 Converting to PDF...")
                        progress_bar.progress(50)
                        
                        pdf_path = Path(temp_dir) / "output.pdf"
                        
                        # Build pandoc command
                        pandoc_cmd = [
                            "pandoc",
                            str(merged_md_path),
                            "-o", str(pdf_path),
                            "--pdf-engine=xelatex",
                            "-V", f"fontsize={font_size}",
                            "-V", f"geometry:margin={margin}",
                            "-V", "linkcolor=blue",
                            "-V", "urlcolor=blue",
                            f"--highlight-style={highlight_style}",
                            "--standalone"
                        ]
                        
                        # Add metadata
                        if pdf_title.strip():
                            pandoc_cmd.extend(["-M", f"title={pdf_title.strip()}"])
                        if pdf_author.strip():
                            pandoc_cmd.extend(["-M", f"author={pdf_author.strip()}"])
                        pandoc_cmd.extend(["-M", f"date={pdf_date.strftime('%B %d, %Y')}"])
                        
                        # Add table of contents if requested
                        if include_toc:
                            pandoc_cmd.extend(["--toc", "--toc-depth=3"])
                        
                        # Handle font selection
                        if font_family == "Auto-detect":
                            # Try to detect and use available fonts
                            fonts_to_try = [
                                ("Liberation Serif", "Liberation Mono"),
                                ("DejaVu Serif", "DejaVu Sans Mono"),
                                ("Times", "Courier"),
                                ("serif", "monospace")  # Generic fallbacks
                            ]
                            
                            font_found = False
                            for main_font, mono_font in fonts_to_try:
                                try:
                                    # Test if font is available by checking fc-list output
                                    result = subprocess.run(
                                        ["fc-list", f":family={main_font}"], 
                                        capture_output=True, text=True
                                    )
                                    if result.returncode == 0 and result.stdout.strip():
                                        pandoc_cmd.extend(["-V", f"mainfont={main_font}"])
                                        pandoc_cmd.extend(["-V", f"monofont={mono_font}"])
                                        font_found = True
                                        break
                                except FileNotFoundError:
                                    # fc-list not available, skip font detection
                                    break
                            
                            # If no fonts found or fc-list not available, use generic fallbacks
                            if not font_found:
                                pandoc_cmd.extend(["-V", "mainfont=serif"])
                                pandoc_cmd.extend(["-V", "monofont=monospace"])
                        
                        elif font_family != "Default":
                            # Use selected font
                            font_mapping = {
                                "Open Sans": ("Open Sans", "DejaVu Sans Mono"),
                                "Liberation Serif": ("Liberation Serif", "Liberation Mono"),
                                "DejaVu Serif": ("DejaVu Serif", "DejaVu Sans Mono"),
                                "Times": ("Times", "Courier")
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
                            
                            with open(pdf_path, "rb") as pdf_file:
                                pdf_data = pdf_file.read()
                                
                                st.success("🎉 PDF conversion completed!")
                                
                                # Generate filename based on title or default
                                if pdf_title.strip():
                                    # Clean title for filename (remove invalid characters)
                                    clean_title = "".join(c for c in pdf_title.strip() if c.isalnum() or c in (' ', '-', '_')).rstrip()
                                    clean_title = clean_title.replace(' ', '_')
                                    output_filename = f"{clean_title}.pdf"
                                else:
                                    output_filename = f"merged_markdown_{len(ordered_files)}_files.pdf"
                                
                                st.download_button(
                                    label="📥 Download PDF",
                                    data=pdf_data,
                                    file_name=output_filename,
                                    mime="application/pdf",
                                    type="primary"
                                )
                                
                                st.balloons()
                
                except FileNotFoundError:
                    st.error("❌ Pandoc not found. Please install Pandoc and XeLaTeX:")
                    st.markdown("""
                    **Installation instructions:**
                    - **Ubuntu/Debian:** `sudo apt-get install pandoc texlive-xetex texlive-fonts-recommended`
                    - **macOS:** `brew install pandoc` + MacTeX
                    - **Windows:** Download from [pandoc.org](https://pandoc.org) + MiKTeX
                    """)
                
                except Exception as e:
                    st.error(f"❌ An error occurred: {str(e)}")
                    st.info("Please check your files and try again")

else:
    st.info("👆 Upload your Markdown files to get started")
    
    # Instructions
    st.markdown("### How to use:")
    st.markdown("""
    1. **Upload** one or more `.md` files from Perplexity AI or other sources
    2. **Reorder** files by selecting them in your preferred sequence
    3. **Customize** PDF formatting options
    4. **Generate** and download your merged PDF for e-readers
    
    The tool preserves original links and formatting while creating a single, readable document.
    """)

# Footer
st.markdown("---")
st.markdown("*Made with ❤️ using Streamlit and Pandoc*")