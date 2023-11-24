import os
import re
import pandas as pd

# Define the functions for reading text files and extracting SNPs
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_vf_and_rs(html_text):
    pattern = r'vf=(\d+)">rs(\d+)'
    matches = re.findall(pattern, html_text)
    return list(set(matches))

# Specify the directory containing the text files
url_dir = 'G:/Aoife/normal'

# Read each text file and create a dictionary mapping SNPs to file names without '.txt'
snp_to_file_dict = {}
url_snp_txt_list = os.listdir(url_dir)
for url in url_snp_txt_list:
    print(url)
    url_snp_path = os.path.join(url_dir, url)
    url_snp_txt = read_text_file(url_snp_path)
    url_snp_list = extract_vf_and_rs(url_snp_txt)
    for vf, rs in url_snp_list:
        snp_id = 'rs' + rs
        snp_to_file_dict[snp_id] = url.replace('.txt', '')  # Remove the '.txt' extension

# Placeholder for the path to your Excel file
excel_path = 'data/processed_SNP_result normal.xlsx'

# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_path)

# Map each SNP id to the corresponding text file name and add a new column with this information
df['Chromosome Id'] = df['SNP id'].map(snp_to_file_dict)

# Save the updated DataFrame back to the Excel file
df.to_excel(excel_path, index=False)
