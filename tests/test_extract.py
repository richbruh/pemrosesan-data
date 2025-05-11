import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Tambahkan parent directory ke sys.path untuk import relatif
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.extract import scrape_page, scrape_all_pages

class TestExtract(unittest.TestCase):
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_success(self, mock_get):
        """Test scrape_page function with successful response"""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.text = """
        <html>
          <body>
            <div class="product-card">
              <h2 class="product-title">Test Product</h2>
              <div class="product-price">$100</div>
              <div class="product-rating">4.5 / 5</div>
              <span class="product-colors">3 Colors</span>
              <span class="product-size">Size: M</span>
              <span class="product-gender">Gender: Unisex</span>
            </div>
          </body>
        </html>
        """
        mock_get.return_value = mock_response
        
        # Test function
        result = scrape_page("https://fashion-studio.dicoding.dev/test")
        
        # Assertions
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['Title'], "Test Product")
        self.assertEqual(result[0]['Price'], "$100")
        self.assertEqual(result[0]['Rating'], "4.5 / 5")
        self.assertEqual(result[0]['Colors'], "3 Colors")
        self.assertEqual(result[0]['Size'], "Size: M")
        self.assertEqual(result[0]['Gender'], "Gender: Unisex")
    
    @patch('utils.extract.requests.get')
    def test_scrape_page_error(self, mock_get):
        """Test scrape_page error handling"""
        # Setup mock to raise an exception
        mock_get.side_effect = Exception("Test connection error")
        
        # Test function
        result = scrape_page("https://fashion-studio.dicoding.dev/test")
        
        # Should return empty list on error
        self.assertEqual(result, [])
    
    @patch('utils.extract.scrape_page')
    def test_scrape_all_pages(self, mock_scrape_page):
        """Test scrape_all_pages function"""
        # Setup mock
        product1 = {'Title': 'Product 1', 'Price': '$50'}
        product2 = {'Title': 'Product 2', 'Price': '$60'}
        mock_scrape_page.side_effect = [[product1], [product2]]
        
        # Test function with 2 pages
        result = scrape_all_pages("https://fashion-studio.dicoding.dev", total_pages=2)
        
        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(mock_scrape_page.call_count, 2)
        
        # Convert result DataFrame back to list for comparison
        result_list = result.to_dict('records')
        self.assertEqual(result_list[0]['Title'], 'Product 1')
        self.assertEqual(result_list[1]['Title'], 'Product 2')

    @patch('utils.extract.time.sleep')  # Mock sleep to speed up tests
    @patch('utils.extract.scrape_page')
    def test_scrape_all_pages_with_delay(self, mock_scrape_page, mock_sleep):
        """Test that scrape_all_pages uses proper delay between requests"""
        # Setup
        mock_scrape_page.return_value = [{'Title': 'Test Product'}]
        
        # Test function
        scrape_all_pages("https://test.com", total_pages=3)
        
        # Verify sleep was called between page requests
        self.assertEqual(mock_sleep.call_count, 3)  # Called once per page


if __name__ == '__main__':
    unittest.main()