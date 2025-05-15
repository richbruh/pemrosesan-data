import unittest
import pandas as pd
import os
import tempfile
from unittest.mock import patch, MagicMock
import sys

# Tambahkan parent directory ke sys.path untuk import relatif
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.load import save_to_csv, save_to_postgres

class TestLoad(unittest.TestCase):
    
    def setUp(self):
        """Setup test data"""
        self.test_df = pd.DataFrame({
            'Title': ['Product A', 'Product B'],
            'Price': [320000.0, 480000.0],
            'Rating': [4.5, 3.8],
            'Colors': [3, 2],
            'Size': ['M', 'L'],
            'Gender': ['Men', 'Women']
        })
    
    def test_save_to_csv(self):
        """Test saving DataFrame to CSV file"""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            temp_filename = tmp.name
            
        try:
            # Test function
            result = save_to_csv(self.test_df, temp_filename)
            
            # Assertions
            self.assertTrue(result)
            self.assertTrue(os.path.exists(temp_filename))
            
            # Check content
            loaded_df = pd.read_csv(temp_filename)
            self.assertEqual(len(loaded_df), 2)
            self.assertEqual(list(loaded_df.columns), list(self.test_df.columns))
            self.assertEqual(loaded_df['Title'].tolist(), ['Product A', 'Product B'])
            
        finally:
            # Cleanup
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    


if __name__ == '__main__':
    unittest.main()