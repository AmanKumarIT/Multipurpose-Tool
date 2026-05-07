import streamlit as st
import io
import os
import tempfile
from PyPDF2 import PdfMerger
from fpdf import FPDF
import pyqrcode
import yt_dlp
from PIL import Image

st.set_page_config(page_title="Multi-Service Tool", page_icon="🛠️", layout="wide")

st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", ["PDF Merger", "Image to PDF", "QR Code Generator", "YouTube Audio Downloader"])

if selection == "PDF Merger":
    st.title("PDF Merger")
    st.write("Upload multiple PDF files to merge them into a single PDF.")
    
    uploaded_files = st.file_uploader("Choose PDF files", type="pdf", accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Merge PDFs"):
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
            
            output = io.BytesIO()
            merger.write(output)
            merger.close()
            
            st.success("PDFs merged successfully!")
            st.download_button(
                label="Download Merged PDF",
                data=output.getvalue(),
                file_name="merged_output.pdf",
                mime="application/pdf"
            )

elif selection == "Image to PDF":
    st.title("Image to PDF Converter")
    st.write("Upload images to convert them into a single PDF.")
    
    uploaded_files = st.file_uploader("Choose Image files", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("Convert to PDF"):
            pdf = FPDF()
            with tempfile.TemporaryDirectory() as tmpdir:
                for idx, img_file in enumerate(uploaded_files):
                    img = Image.open(img_file)
                    # Convert to RGB if not
                    if img.mode != 'RGB':
                        img = img.convert('RGB')
                    
                    # Save image temporarily
                    img_path = os.path.join(tmpdir, f"img_{idx}.jpg")
                    img.save(img_path)
                    
                    pdf.add_page()
                    pdf.image(img_path, x=10, y=10, w=180)
                
                pdf_output_path = os.path.join(tmpdir, "output.pdf")
                pdf.output(pdf_output_path)
                
                with open(pdf_output_path, "rb") as f:
                    pdf_bytes = f.read()
                    
            st.success("Images converted to PDF successfully!")
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name="images_output.pdf",
                mime="application/pdf"
            )

elif selection == "QR Code Generator":
    st.title("QR Code Generator")
    st.write("Enter a link or text to generate a QR Code.")
    
    link_input = st.text_input("Enter link or text:")
    
    if st.button("Generate QR Code"):
        if link_input:
            url = pyqrcode.create(link_input)
            output = io.BytesIO()
            url.png(output, scale=6)
            output.seek(0)
            
            st.image(output, caption="Generated QR Code")
            
            st.download_button(
                label="Download QR Code",
                data=output.getvalue(),
                file_name="qrcode.png",
                mime="image/png"
            )
        else:
            st.error("Please enter a link or text.")

elif selection == "YouTube Audio Downloader":
    st.title("YouTube Audio Downloader")
    st.write("Enter a YouTube link to download the audio.")
    
    yt_link = st.text_input("Enter YouTube link:")
    
    if st.button("Download Audio"):
        if yt_link:
            with st.spinner("Downloading audio..."):
                with tempfile.TemporaryDirectory() as tmpdir:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(tmpdir, '%(title)s.%(ext)s'),
                        'quiet': True,
                        'cookiefile': 'cookies.txt',
                        'noplaylist': True,
                        'extractaudio': True,
                        'audioformat': 'mp3'
                    }
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(yt_link, download=True)
                            filename = ydl.prepare_filename(info)
                            
                        if os.path.exists(filename):
                            with open(filename, "rb") as f:
                                audio_bytes = f.read()
                            
                            st.success("Download complete!")
                            st.download_button(
                                label="Save Audio",
                                data=audio_bytes,
                                file_name=os.path.basename(filename),
                                mime="application/octet-stream"
                            )
                        else:
                            st.error("Failed to find the downloaded file.")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter a YouTube link.")
