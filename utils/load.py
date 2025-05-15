def save_to_csv(df, file_path='products.csv'):
    try: 
        # Tambahkan pengecekan DataFrame kosong
        if df is None or df.empty:
            print("DataFrame kosong, tidak ada data untuk disimpan")
            return False
            
        # Save DataFrame dan di load dalam bentuk CSV
        import os
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Simpan ke CSV (indentasi diperbaiki)
        df.to_csv(file_path, index=False)
        print(f"Data berhasil disimpan ke {file_path}")
        
        # Verifikasi file berhasil dibuat
        if os.path.exists(file_path):
            print(f"File berhasil dibuat: {file_path}")
            print(f"Ukuran file: {os.path.getsize(file_path)} bytes")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False
    
def save_to_postgres(df, table_name='products', conn=None):
    try:
        # Cek apakah DataFrame kosong
        if df is None or df.empty:
            print("DataFrame kosong, tidak ada data untuk disimpan")
            return False
        
        # Simpan DataFrame ke PostgreSQL
        if conn is None:
            print("Koneksi database tidak tersedia")
            return False
        
        # Simpan DataFrame ke PostgreSQL
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Data berhasil disimpan ke tabel {table_name} di PostgreSQL")
        
        return True
    except Exception as e:
        print(f"Error saving to PostgreSQL: {e}")
        return False
    
