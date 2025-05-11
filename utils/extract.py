import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_page(url):
    """
    Scrape a single page of the Fashion Studio website.
    
    Args:
        url (str): The URL of the page to scrape
        
    Returns:
        list: List of dictionaries containing product data
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        # Find all product cards
        product_cards = soup.find_all('div', class_='product-card')
        
        for card in product_cards:
            try:
                # Extract product data
                title = card.find('h3', class_='product-title').text.strip()
                
                # Extract price (handle cases where price might be unavailable)
                price_element = card.find('div', class_='product-price')
                if price_element and '$' in price_element.text:
                    price = price_element.text.strip()
                else:
                    price = "Price Unavailable"
                
                # Extract rating
                rating_element = card.find('div', class_='product-rating')
                rating = rating_element.text.strip() if rating_element else "Invalid Rating"
                
                # Extract colors
                colors_element = card.find('span', class_='product-colors')
                colors = colors_element.text.strip() if colors_element else "Unknown"
                
                # Extract size
                size_element = card.find('span', class_='product-size')
                size = size_element.text.strip() if size_element else "Unknown"
                
                # Extract gender
                gender_element = card.find('span', class_='product-gender')
                gender = gender_element.text.strip() if gender_element else "Unknown"
                
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
        url = f"{base_url}?page={page}"
        print(f"Scraping page {page}/{total_pages}...")
        
        products = scrape_page(url)
        all_products.extend(products)
        
        # Add a small delay to avoid overloading the server
        time.sleep(1)
    
    return pd.DataFrame(all_products)

# Test the extraction
base_url = "https://fashion-studio.dicoding.dev"
df = scrape_all_pages(base_url, total_pages=2)  # Just 2 pages for testing
df.head()