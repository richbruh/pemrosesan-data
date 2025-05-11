import unittest
import pandas as pd
import os
import tempfile
from unittest.mock import patch, MagicMock
import sys

# Tambahkan parent directory ke sys.path untuk import relatif
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.load import save_to_csv, save_to_google_sheets, save_to_postgresql

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
    
    def test_save_to_csv_error(self):
        """Test error handling when saving to CSV fails"""
        # Test with invalid path to trigger error
        invalid_path = "/invalid_directory/test.csv"
        
        # Function should return False on error
        result = save_to_csv(self.test_df, invalid_path)
        self.assertFalse(result)
    
    @patch('utils.load.create_engine')
    def test_save_to_postgresql(self, mock_create_engine):
        """Test saving DataFrame to PostgreSQL"""
        # Setup mock
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_to_sql = MagicMock()
        self.test_df.to_sql = mock_to_sql
        
        # Test function
        result = save_to_postgresql(self.test_df, 'postgresql://test:test@localhost/testdb')
        
        # Assertions
        self.assertTrue(result)
        mock_create_engine.assert_called_once()
        mock_to_sql.assert_called_once()
    
    @patch('utils.load.create_engine')
    def test_save_to_postgresql_error(self, mock_create_engine):
        """Test error handling when saving to PostgreSQL fails"""
        # Setup mock to raise exception
        mock_create_engine.side_effect = Exception("Database connection error")
        
        # Function should return False on error
        result = save_to_postgresql(self.test_df, 'postgresql://test:test@localhost/testdb')
        self.assertFalse(result)
    
    @patch('utils.load.build')
    @patch('utils.load.Credentials')
    def test_save_to_google_sheets(self, mock_credentials, mock_build):
        """Test saving DataFrame to Google Sheets"""
        # Setup mocks
        mock_service = MagicMock()
        mock_sheets = MagicMock()
        mock_values = MagicMock()
        mock_update = MagicMock()
        
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheets
        mock_sheets.values.return_value = mock_values
        mock_values.update.return_value = mock_update
        mock_update.execute.return_value = {'updatedCells': 12}
        
        # Test function
        result = save_to_google_sheets(self.test_df, 'test_spreadsheet_id')
        
        # Assertions
        self.assertTrue(result)
        mock_build.assert_called_once_with('sheets', 'v4', credentials=mock_credentials.from_service_account_file.return_value)
        mock_values.update.assert_called_once()


if __name__ == '__main__':
    unittest.main()