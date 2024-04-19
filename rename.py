import os
import re
import PyPDF2

def find_string_in_pdf(file_path):
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        first_page = reader.pages[0]
        text = first_page.extract_text()

    pattern = r'\bD(\d+\.\d+|\.\d+\.\d+)|Deliverable (\d+\.\d+)\b'
    match = re.search(pattern, text)
    
    if match:
        # Return the full matched string, suitable for dictionary lookup
        return match.group().replace('Deliverable ', 'D')
    return None

def unique_file_name(folder_path, base_name):
    counter = 1
    new_name = base_name
    while os.path.exists(os.path.join(folder_path, f'{new_name}.pdf')):
        new_name = f"{base_name}_{counter}"
        counter += 1
    return new_name

# Dictionary to hold the mapping of Del Rel. No to Title
deliverables = {
    "D1.2":"1st Project management and activity progress report",
    "D1.3":"2nd Project management and activity progress report",
    "D1.8":"1st Project financial report",
    "D1.9":"2nd Project financial report",
    "D1.10":"3rd Project financial report",
    #...
}

# Path to the folder containing the PDF files
folder_path = './'

for filename in os.listdir(folder_path):
    if filename.endswith('.pdf'):
        file_path = os.path.join(folder_path, filename)
        deliverable_number = find_string_in_pdf(file_path)

        if deliverable_number and deliverable_number in deliverables:
            title = deliverables[deliverable_number]
            new_base_name = f"{deliverable_number} {title}"  # Construct new base name with number and title
            new_name = unique_file_name(folder_path, new_base_name)
            new_file_path = os.path.join(folder_path, f'{new_name}.pdf')
            os.rename(file_path, new_file_path)
            print(f'Renamed "{filename}" to "{new_name}.pdf"')
        else:
            print(f'No matching string found or deliverable not listed in "{filename}"')
