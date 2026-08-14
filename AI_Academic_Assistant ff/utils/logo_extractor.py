import fitz  # PyMuPDF
import os


class LogoExtractor:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_logo(self, output_folder="generated"):

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        doc = fitz.open(self.pdf_path)

        image_count = 0

        for page_num in range(len(doc)):

            page = doc.load_page(page_num)

            image_list = page.get_images(full=True)

            if not image_list:
                continue

            for img in image_list:

                xref = img[0]

                base_image = doc.extract_image(xref)

                image_bytes = base_image["image"]

                image_ext = base_image["ext"]

                image_path = os.path.join(
                    output_folder,
                    f"logo.{image_ext}"
                )

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                image_count += 1

                # Return only the first image
                return image_path

        return None