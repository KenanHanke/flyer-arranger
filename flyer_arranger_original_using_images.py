#!/usr/bin/env python3

import argparse
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import io
from pdf2image import convert_from_path

def add_a5_to_a4(writer, page_image, page_number):
    # A4 landscape dimensions
    a4_width, a4_height = A4[1], A4[0]  # Switch width and height for landscape
    
    # Create a PDF canvas for the new A4 page
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=(a4_width, a4_height))
    x_positions = [0, a4_width / 2]  # Positions to place the A5 pages

    if page_number % 2 == 1:
        # Rotate canvas for the second page
        c.translate(a4_width / 2, a4_height)
        c.rotate(180)

    # Place the A5 page image twice side by side
    for x in x_positions:
        c.drawInlineImage(page_image, x - (a4_width / 2 if page_number % 2 == 1 else 0), 0, width=a4_width / 2, height=a4_height)

    c.save()
    
    # Move the "packet" data to a PDF page
    packet.seek(0)
    new_pdf = PdfReader(packet)
    writer.add_page(new_pdf.pages[0])

def process_pdf(input_pdf_path, output_pdf_path):
    # Convert entire PDF to images
    images = convert_from_path(input_pdf_path, dpi=250)

    writer = PdfWriter()

    # Add images to the PDF, flipping every second one
    for index, page_image in enumerate(images):
        # Add this A5 page image twice onto an A4 landscape page, flipping every second page
        add_a5_to_a4(writer, page_image, index)

    # Write the output PDF
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

def main():
    parser = argparse.ArgumentParser(description='Convert A5 PDF to A4 layout PDF with upside-down flipping for long edge binding.')
    parser.add_argument('input_pdf', type=str, help='Path to the input PDF file.')
    parser.add_argument('-o', '--output_pdf', type=str, help='Path to the output PDF file. If not provided, defaults to <input_pdf>_with_A4_layout.pdf')
    
    args = parser.parse_args()
    
    input_pdf_path = args.input_pdf
    output_pdf_path = args.output_pdf if args.output_pdf else os.path.splitext(input_pdf_path)[0] + '_with_A4_layout.pdf'
    
    process_pdf(input_pdf_path, output_pdf_path)
    print(f'Output PDF saved to {output_pdf_path}')

if __name__ == '__main__':
    main()
