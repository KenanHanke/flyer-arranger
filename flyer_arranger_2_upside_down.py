#!/usr/bin/env python3

import argparse
import os
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter, PageObject, Transformation

def add_a5_to_a4(writer, page, rotate=False):
    # A4 landscape dimensions
    a4_width, a4_height = A4[1], A4[0]  # Switch width and height for landscape

    # Create a new A4 landscape page
    new_page = PageObject.create_blank_page(width=a4_width, height=a4_height)

    # Define the positions for placing the A5 pages side by side on the A4 page
    x_positions = [0, a4_width / 2]

    for x in x_positions:
        # Create a blank page with the same dimensions as the A5 page
        page_copy = PageObject.create_blank_page(width=a4_width / 2, height=a4_height)
        
        # Merge the original page into the copy
        page_copy.merge_page(page)
        
        # Rotate the page copy if required
        if rotate:
            # First translate the page so that the center is at the origin
            translation_to_origin = Transformation().translate(tx=-a4_width / 4, ty=-a4_height / 2)
            page_copy.add_transformation(translation_to_origin)
            
            # Rotate the page
            rotation = Transformation().rotate(180)
            page_copy.add_transformation(rotation)
            
            # Translate the page back to its original position
            translation_back = Transformation().translate(tx=a4_width / 4, ty=a4_height / 2)
            page_copy.add_transformation(translation_back)
        
        # Translate the page copy to the correct position
        translation = Transformation().translate(tx=x, ty=0)
        new_page.add_transformation(translation)
        new_page.merge_page(page_copy)

    writer.add_page(new_page)

def process_pdf(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Add each A5 page to the PDF, duplicating it side by side on A4
    for i, page in enumerate(reader.pages):
        rotate = (i == 1)  # Rotate the second page
        add_a5_to_a4(writer, page, rotate=rotate)

    # Write the output PDF
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

def main():
    parser = argparse.ArgumentParser(description='Convert A5 PDF to A4 layout PDF with pages side by side.')
    parser.add_argument('input_pdf', type=str, help='Path to the input PDF file.')
    parser.add_argument('-o', '--output_pdf', type=str, help='Path to the output PDF file. If not provided, defaults to <input_pdf>_with_A4_layout.pdf')

    args = parser.parse_args()

    input_pdf_path = args.input_pdf
    output_pdf_path = args.output_pdf if args.output_pdf else os.path.splitext(input_pdf_path)[0] + '_with_A4_layout.pdf'

    process_pdf(input_pdf_path, output_pdf_path)
    print(f'Output PDF saved to {output_pdf_path}')

if __name__ == '__main__':
    main()
