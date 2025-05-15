import sys
import os

# Tambahkan direktori root ke sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
from utils.extract import scrape_all_pages
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_postgres


def run_etl_pipeline():
    """
    Menjalankan seluruh pipeline ETL.
    """
    print("Memulai pipeline ETL...")
    
    # Ekstraksi
    print("\n[1/3] Mengekstrak data dari website Fashion Studio...")
    base_url = "https://fashion-studio.dicoding.dev"
    raw_data = scrape_all_pages(base_url, total_pages=50)
    print(f"Berhasil mengekstrak {len(raw_data)} data produk.")
    
    # Transformasi
    print("\n[2/3] Mentransformasi data...")
    
    transformed_data = transform_data(raw_data)
    print(f"Data hasil transformasi berisi {len(transformed_data)} data bersih.")
    print(transformed_data.head())
    # Loading
    print("\n[3/3] Menyimpan data ke repositori...")
    
    # Simpan ke CSV (Wajib)
    save_to_csv(transformed_data, 'products.csv')
    save_to_postgres(transformed_data, 'products', conn=None)
    print("\nPipeline ETL berhasil dijalankan!")

# Untuk menjalankan script
if __name__ == "__main__":
    run_etl_pipeline()
    