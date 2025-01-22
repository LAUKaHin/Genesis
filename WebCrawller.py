import os
import time
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests


def configure_logging():
    """Configure logging for the script."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )


def initialize_webdriver():
    """Initialize and return a Selenium WebDriver."""
    options = Options()
    options.headless = True  # Run in headless mode for efficiency
    return webdriver.Firefox(options=options)


def save_images(img_elements, folder_path):
    """Save images from the provided img elements to the specified folder."""
    os.makedirs(folder_path, exist_ok=True)
    image_links = []

    for img in img_elements:
        img_url = img['src']
        img_name = os.path.basename(img_url)
        img_path = os.path.join(folder_path, img_name)

        try:
            response = requests.get(img_url, stream=True)
            if response.status_code == 200:
                with open(img_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                image_links.append((img_url, img_path))
        except Exception as e:
            logging.error(f"Error saving image {img_url}: {e}")

    return image_links


def scrape_product_details(driver, base_url, product_code, output_folder, gcl_to_color):
    """Scrape details for a single product."""
    url = f"{base_url}{product_code}"
    product_folder = os.path.join(output_folder, product_code)
    markdown_file = os.path.join(product_folder, f"{product_code}.md")
    os.makedirs(product_folder, exist_ok=True)

    try:
        logging.info(f"Processing URL: {url}")
        driver.get(url)
        time.sleep(3)  # Allow page to load

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract details
        product_name = soup.select_one('.gu-product-detail-list-title').text.strip() if soup.select_one('.gu-product-detail-list-title') else "N/A"
        price = soup.select_one('.h-currency').text.strip() if soup.select_one('.h-currency') else "N/A"
        description = soup.select_one('.product-desc').text.strip() if soup.select_one('.product-desc') else "N/A"
        material = soup.select_one('.desc-content').text.strip() if soup.select_one('.desc-content') else "N/A"

        # Extract sizes
        size_elements = soup.select('ul.sku-select-sizes li')
        available_sizes = [size.text.strip() for size in size_elements if "active" in size.get("class", [])]
        unavailable_sizes = [size.text.strip() for size in size_elements if "active" not in size.get("class", [])]

        # Extract colors
        color_elements = soup.select('ul.sku-select-colors li img')
        colors = []
        for img in color_elements:
            src = img['src']
            gcl_code = src.split('/')[-1].split('.')[0]
            color_name = gcl_to_color.get(gcl_code, gcl_code)
            colors.append(f"{color_name}: ![Color Image]({src})")

        # Extract gallery images
        gallery_elements = soup.select('ul.picture-viewer-bottom li img')
        gallery_links = save_images(gallery_elements, product_folder)

        # Generate Markdown content
        markdown_content = (
            f"# {product_name}\n\n"
            f"**URL:** [{url}]({url})\n\n"
            f"**Price:** {price}\n\n"
            f"**Description:**\n{description}\n\n"
            f"**Material:**\n{material}\n\n"
            f"**Colors:**\n" + "\n".join(colors) + "\n\n"
            f"**Available Sizes:** {', '.join(available_sizes) if available_sizes else 'No available sizes'}\n\n"
            f"**Unavailable Sizes:** {', '.join(unavailable_sizes) if unavailable_sizes else 'No unavailable sizes'}\n\n"
            f"**Gallery Images:**\n" + "\n".join([f"![Gallery Image]({link[0]})" for link in gallery_links]) + "\n"
        )

        # Save Markdown file
        with open(markdown_file, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
        logging.info(f"Saved: {markdown_file}")

    except Exception as e:
        logging.error(f"Error processing URL {url}: {e}")


def main():
    configure_logging()

    base_url = "https://www.gu-global.com/hk/zh_HK/product-detail.html?productCode="
    output_folder = "./GU_Product_Details"
    start_code, end_code = 121, 4000

    # GCL to color mapping
    gcl_to_color = {
        "GCL00": "White",
        "GCL01": "Off White",
        "GCL02": "Light Gray",
        "GCL03": "Gray",
        # Add more mappings as needed
    }

    driver = initialize_webdriver()

    try:
        for code in range(start_code, end_code + 1):
            product_code = f"u000000000{str(code).zfill(4)}"
            scrape_product_details(driver, base_url, product_code, output_folder, gcl_to_color)
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
