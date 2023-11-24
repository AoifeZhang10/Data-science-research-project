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

    return matches


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
import time


def scrape_genetic_data(url):
    # 设置Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # loading website
        driver.get(url)

        # Waiting for loading website time
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "pie_chart_holder"))
        )
        # Wait additional time to ensure page is fully loaded
        # Comply with website requirements to avoid malicious crawling by spider
        time.sleep(30)  # waiting 30 seconds

        # Get web page source code
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # save result to dict
        population_data = {}

        # Extract all parts containing the chart
        pie_chart_divs = soup.find_all("div", class_="pie_chart_holder")

        for div in pie_chart_divs:
            population_name = div.find("span", class_="_ht ht").text.strip()
            values = div.find_all("text", style=lambda value: value and 'text-anchor: start;' in value)

            if population_name in ["EUR", "ASW", "ESN", "GWD", "MSL", "YRI"]:
                pop_data = {}
                for value in values:
                    allele, freq = value.text.strip().split(': ')
                    pop_data[allele] = freq

                population_data[population_name] = pop_data

        return population_data

    finally:
        # Close webpage
        driver.quit()


def AFR_calculate(data):
    # Convert percentage to float
    for region in data:
        for allele in data[region]:
            data[region][allele] = float(data[region][allele].replace('%', '')) / 100

    african_regions = ['ESN', 'GWD', 'MSL', 'YRI']
    sum_nucleotides = {nt: 0 for nt in ['G', 'A', 'T', 'C']}  # 初始化核苷酸总和

    # Calculate the sum of each SNP in Africa
    for region in african_regions:
        for nt in sum_nucleotides:
            sum_nucleotides[nt] += data[region].get(nt, 0)

    avg_nucleotides = {nt: total / len(african_regions) for nt, total in sum_nucleotides.items()}
    data['AFR'] = avg_nucleotides
    return data


def process_and_save_data(snp_id, data, file_name='SNP_result normal 7_8_16_17_20.xlsx'):
    if len(data['EUR']) != 0:
        data['SNP id'] = str(snp_id)
        # Remove the sub-African SNP
        for region in ["ESN", "GWD", "MSL", "YRI"]:
            data.pop(region, None)

        # Only the category with the highest proportion is retained in the EUR (A,T,C,G)
        eur_max_allele = max(data['EUR'], key=data['EUR'].get)
        data['EUR'] = {eur_max_allele: data['EUR'][eur_max_allele]}

        # Ensure that categories in ASW and AFR are consistent with EUR
        for region in ['ASW', 'AFR']:
            if eur_max_allele in data[region]:
                data[region] = {eur_max_allele: data[region][eur_max_allele]}
            else:
                data[region] = {eur_max_allele: 0}

        new_data = pd.DataFrame(data)

        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # save
        updated_data.to_excel(file_name, index=False)
        return 'success'
    else:
        return None


url_dir = 'data/y_Chromosome'

url_snp_txt_list = os.listdir(url_dir)

for url in url_snp_txt_list:
    print(url)
    url_snp_path = os.path.join(url_dir, url)
    url_snp_txt = read_text_file(url_snp_path)
    url_snp_list = extract_vf_and_rs(url_snp_txt)
    print(url_snp_list)
    number_snp = len(url_snp_list)
    print(number_snp)
    start_num = 0
    for index, data in url_snp_list:
        print(start_num)  # Assuming 'number_snp' was intended to be 'index + start_num'
        snp_id = 'rs' + str(data[1])
        vf = str(data[0])
        max_attempts = 5
        # 要抓取的URL
        url = f'https://asia.ensembl.org/Homo_sapiens/Variation/Population?db=core;g=ENSG00000135744;r=1:230690776-230745576;v={snp_id};vdb=variation;vf={vf}#population_freq_AFR'
        print(url)
        # Loop to attempt the process up to max_attempts times
        for attempt in range(max_attempts):
            try:
                # Scrape the data
                data = scrape_genetic_data(url)
                print(data)

                # Calculate the data
                data = AFR_calculate(data)
                print(data)

                # Process and save the data
                result = process_and_save_data(snp_id, data)

                # If the process_and_save_data function does not return None, break the loop
                if result != None:
                    break
            except Exception as e:
                print(f"An error occurred during attempt {attempt + 1}: {e}")

            # Optional: Print the attempt number
            print(f"Attempt {attempt + 1} completed")

        # Check if the loop completed all attempts without breaking
        if attempt == max_attempts - 1:
            print("Maximum attempts reached without success.")

        start_num = start_num + 1
