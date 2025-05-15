import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_page(url):
    try:
        print(f"Fetching {url}...")
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Find all product cards
        product_cards = soup.find_all('div', class_='collection-card')
        print(f"Found {len(product_cards)} product cards on page")
        
        for card in product_cards:
            try:
                # Extract product data
                title = card.find('h3', class_='product-title').text.strip()
                
                # Extract price - update selector
                price_element = card.find('span', class_='price')
                if price_element and '$' in price_element.text:
                    price = price_element.text.strip()
                else:
                    price = "Price Unavailable"
                
                # Extract paragraphs that contain other info
                paragraphs = card.find_all('p')
                
                # Initialize default values
                rating = "Invalid Rating"
                colors = "Unknown"
                size = "Unknown"
                gender = "Unknown"
                
                # Process each paragraph to extract info
                for p in paragraphs:
                    text = p.text.strip()
                    if "Rating:" in text:
                        rating = text.replace("Rating:", "").strip()
                    elif "Colors" in text:
                        colors = text
                    elif "Size:" in text:
                        size = text
                    elif "Gender:" in text:
                        gender = text
                
                # Add timestamp for when data was scraped
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                products.append({
                    'Title': title,
                    'Price': price,
                    'Rating': rating,
                    'Colors': colors,
                    'Size': size,
                    'Gender': gender,
                    'Timestamp': timestamp
                })
                
            except Exception as e:
                print(f"Error extracting product data: {e}")
                continue
        
        return products
    
    except Exception as e:
        print(f"Error scraping page: {e}")
        return []

def scrape_all_pages(base_url, total_pages=50):
    """
    Scrape all pages from Fashion Studio website.
    
    Args:
        base_url (str): Base URL of the website
        total_pages (int): Total number of pages to scrape
    
    Returns:
        pd.DataFrame: DataFrame containing all product data
    """
    all_products = []
    

    for page in range(1, total_pages + 1):
        if page == 1:
            url = base_url
        else:
            url = f"{base_url}/page{page}"
        print(f"Scraping page {page}/{total_pages}...")
        
        products = scrape_page(url)
        print(f"Found {len(products)} products on page {page}")
        all_products.extend(products)
        
        # Add a small delay to avoid overloading the server
        time.sleep(1)
    
    df = pd.DataFrame(all_products)
    print(f"Total products extracted: {len(df)}")
    return df

if __name__ == "__main__":
    # Test the extraction
    base_url = "https://fashion-studio.dicoding.dev"
    df = scrape_all_pages(base_url, total_pages=50)  # Just 50 pages
    print(df.head())