import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    
    def setUp(self):
        # Siapkan data untuk testing
        self.test_data = pd.DataFrame({
            'Title': ['Product A', 'Unknown Product'],
            'Price': ['$20', 'Price Unavailable'],
            'Rating': ['4.5 / 5', 'Invalid Rating'],
            'Colors': ['3 Colors', '1 Colors'],
            'Size': ['Size: M', 'Size: L'],
            'Gender': ['Gender: Men', 'Gender: Women']
        })
    
    def test_transform_data(self):
        # Panggil fungsi transform
        result = transform_data(self.test_data)
        
        # Verifikasi hasil transformasi
        self.assertFalse('Unknown Product' in result['Title'].values)
        self.assertTrue(all(isinstance(x, float) for x in result['Price']))
        self.assertTrue(all(isinstance(x, float) for x in result['Rating']))
        self.assertTrue(all(isinstance(x, int) for x in result['Colors']))
        
    def test_price_conversion(self):
        # Test khusus konversi USD ke IDR
        result = transform_data(pd.DataFrame({
            'Title': ['Product A'],
            'Price': ['$100'],
            'Rating': ['4.5 / 5'],
            'Colors': ['3 Colors'],
            'Size': ['Size: M'],
            'Gender': ['Gender: Men']
        }))
        self.assertEqual(result['Price'].iloc[0], 1600000.0)  # $100 * 16000

if __name__ == '__main__':
    unittest.main()