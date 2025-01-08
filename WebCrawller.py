from selenium import webdriver
from bs4 import BeautifulSoup
import os
import time
from googletrans import Translator
import requests

def translate_table(html_table):
    translator = Translator()

    # Parse the HTML table using BeautifulSoup
    soup = BeautifulSoup(html_table, 'html.parser')
    table = soup.select_one('table.sizechartTb.ke-zeroborder.k-table')
    
    if not table:
        print("Table not found!")
        return "**No size chart available**"

    # Extract headers and rows
    headers = [th.get_text(strip=True) for th in table.select('th')]
    rows = []
    for tr in table.select('tr'):
        row = [td.get_text(strip=True) for td in tr.select('td')]
        if row:
            rows.append(row)

    # Translate headers
    translated_headers = [translator.translate(header, src='zh-cn', dest='en').text for header in headers]

    # Translate rows
    translated_rows = []
    for row in rows:
        translated_row = [translator.translate(cell, src='zh-cn', dest='en').text for cell in row]
        translated_rows.append(translated_row)

    # Generate table in Markdown format
    markdown_table = ""
    markdown_table += "| " + " | ".join(translated_headers) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(translated_headers)) + " |\n"
    for translated_row in translated_rows:
        markdown_table += "| " + " | ".join(translated_row) + " |\n"

    return markdown_table

def save_images(img_elements, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    image_links = []

    for img in img_elements:
        img_url = img['src']
        img_name = os.path.basename(img_url)
        img_path = os.path.join(folder_path, img_name)

        # Download and save the image
        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                with open(img_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                image_links.append((img_url, img_path))
        except Exception as e:
            print(f"Error saving image {img_url}: {e}")

    return image_links

def scrape_product_details_with_selenium(base_url, start, end, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Initialize WebDriver
    driver = webdriver.Chrome()  # Ensure you have ChromeDriver installed

    # GCL to color name mapping (example for demonstration; expand as needed)
    gcl_to_color = {
    "GCL00": "White",
    "GCL01": "Off White",
    "GCL02": "Light Gray",
    "GCL03": "Gray",
    "GCL04": "Gray",
    "GCL05": "Gray",
    "GCL07": "Gray",
    "GCL08": "Dark Gray",
    "GCL09": "Black",
    "GCL10": "Pink",
    "GCL11": "Pink",
    "GCL12": "Pink",
    "GCL14": "Red",
    "GCL15": "Red",
    "GCL17": "Red",
    "GCL18": "Wine",
    "GCL24": "Orange",
    "GCL25": "Orange",
    "GCL26": "Orange",
    "GCL28": "Dark Orange",
    "GCL30": "Natural",
    "GCL31": "Beige",
    "GCL32": "Beige",
    "GCL33": "Khaki",
    "GCL35": "Brown",
    "GCL38": "Dark Brown",
    "GCL39": "Dark Brown",
    "GCL41": "Yellow",
    "GCL42": "Yellow",
    "GCL43": "Yellow",
    "GCL49": "Mustard",
    "GCL52": "Green",
    "GCL53": "Green",
    "GCL54": "Green",
    "GCL55": "Green",
    "GCL56": "Olive",
    "GCL57": "Olive",
    "GCL58": "Dark Green",
    "GCL59": "Dark Green",
    "GCL60": "Light Blue",
    "GCL61": "Blue",
    "GCL62": "Blue",
    "GCL63": "Blue",
    "GCL64": "Blue",
    "GCL65": "Blue",
    "GCL67": "Blue",
    "GCL68": "Blue",
    "GCL69": "Navy",
    "GCL72": "Purple",
    "GCL73": "Purple",
    "GCL75": "Purple",
    "GCL76": "Purple",
    "GCL80": "Unknown",
    "GCL81": "Unknown",
}

    for i in range(start, end + 1):
        product_code = f"u000000000{str(i).zfill(4)}"
        url = f"{base_url}{product_code}"
        product_folder = os.path.join(output_folder, product_code)
        markdown_file = os.path.join(product_folder, f"{product_code}.md")

        try:
            # Load the page using Selenium
            driver.get(url)
            time.sleep(3)  # Wait for the page to load

            # Parse the loaded page with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Ignore sold out or not exist
            if("缺貨" in str(soup) or "找不到頁面！" in str(soup) or "已售罄" in str(soup)):
                continue
            
            # Extract product details
            product_name_element = soup.select_one('.gu-product-detail-list-title')
            product_name = product_name_element.text.strip() if product_name_element else "N/A"

            price_element = soup.select_one('.h-currency')
            price = price_element.text.strip() if price_element else "N/A"

            description_element = soup.select_one('.product-desc')
            description_cn = description_element.text.strip() if description_element else "N/A"

            material_element = soup.select_one('.desc-content')
            material = material_element.text.strip() if material_element else "N/A"

            # Extract sizes and their availability
            size_elements = soup.select('ul.sku-select-sizes li')
            sizes = []
            unavailable_sizes = []
            for size in size_elements:
                size_text = size.text.strip()  # Extract the size text
                if "active" in size.get("class", []):
                    sizes.append(size_text)
                else:
                    unavailable_sizes.append(size_text)

            # Extract colors
            color_elements = soup.select('ul.sku-select-colors li img')
            colors = []
            for img in color_elements:
                src = img['src']
                gcl_code = src.split('/')[-1].split('.')[0]  # Extract GCL code from filename
                color_name = gcl_to_color.get(gcl_code, gcl_code)  # Map GCL code to color name
                colors.append(f"{color_name}: ![Color Image]({src})")

            # Extract gallery images
            gallery_elements = soup.select('ul.picture-viewer-bottom li img')
            gallery_links = save_images(gallery_elements, product_folder)

            # Extract size chart
            size_chart_element = soup.select_one('table.sizechartTb.ke-zeroborder.k-table')
            size_chart = ""
            if size_chart_element:
                size_chart = translate_table(str(size_chart_element))
            else:
                size_chart = "**No size chart available**"

            # Generate Markdown content
            markdown_content = (
                f"# {product_name}\n\n"
                f"**URL:** [{url}]({url})\n\n"
                f"**Price:** {price}\n\n"
                f"**Description:**\n{description_cn}\n\n"
                f"**Material:**\n{material}\n\n"
                f"**Colors:**\n" + "\n".join(colors) + "\n\n"
                f"**Available Sizes:** {', '.join(sizes) if sizes else 'No available sizes'}\n\n"
                f"**Unavailable Sizes:** {', '.join(unavailable_sizes) if unavailable_sizes else 'No unavailable sizes'}\n\n"
                f"**Gallery Images:**\n" + "\n".join([f"![Gallery Image]({link[0]})" for link in gallery_links]) + "\n\n"
                f"**Size Chart:**\n\n{size_chart}\n"
            )

            # Save the Markdown file
            with open(markdown_file, 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            print(f"Saved: {markdown_file}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

    driver.quit()

# Define base URL and output folder
base_url = "https://www.gu-global.com/hk/zh_HK/product-detail.html?productCode="
output_folder = "./GU_Product_Details"

# Scrape product details for product codes 0121 to 4000
scrape_product_details_with_selenium(base_url, 512, 4000, output_folder)
