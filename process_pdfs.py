import os
import fitz

input_folder = "input"
output_folder = "output"

os.makedirs(output_folder, exist_ok=True)

for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        input_pdf = fitz.open(input_path)
        output_pdf = fitz.open()
        previous_last_line = "ЫЫЫЫЫЫ"
        current_slide_pages = []
        for page_num in range(len(input_pdf)):
            page = input_pdf.load_page(page_num)
            text = page.get_text("text")
            lines = text.strip().splitlines()
            current_last_line = lines[-1].strip() if lines else ""
            if current_last_line and current_last_line == previous_last_line:
                current_slide_pages.append(page)
            else:
                if current_slide_pages:
                    last_page_of_slide = current_slide_pages[-1]
                    output_pdf.insert_pdf(
                        input_pdf,
                        from_page=last_page_of_slide.number,
                        to_page=last_page_of_slide.number,
                    )
                current_slide_pages = [page]
                previous_last_line = current_last_line
        if current_slide_pages:
            last_page_of_slide = current_slide_pages[-1]
            output_pdf.insert_pdf(
                input_pdf,
                from_page=last_page_of_slide.number,
                to_page=last_page_of_slide.number,
            )
        output_pdf.save(output_path, garbage=4, deflate=True)
        input_pdf.close()
        output_pdf.close()

print("Файлы сохранены в папке:", output_folder)
