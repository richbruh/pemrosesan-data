def transform_data(df):
    """
    Transform scraped data to ensure quality and consistency.
    
    Args:
        df (pd.DataFrame): Raw data from web scraping
        
    Returns:
        pd.DataFrame: Transformed and cleaned data
    """
    # Buat salinan dataframe untuk transformasi
    df_transformed = df.copy()
    print(f"Raw Data {(df_transformed.head())} before cleaning.")
    try:
        # 1. Convert price from USD to IDR (exchange rate: Rp16,000)
        def convert_price_to_idr(price):
            try:
                if price == "Price Unavailable":
                    return None
                price_value = float(price.replace("$", "").strip())
                # Convert to IDR
                return price_value * 16000
            
            except Exception as e:
                print(f"Error converting price: {e}")
                return None
                
        
        df_transformed['Price'] = df_transformed['Price'].apply(convert_price_to_idr)
        print(f"Transformed Data {(df_transformed.head())} after Price Cleaning.")
        # 2. Clean Rating column
        def clean_rating(rating):
            try:
                if "Rating:" in rating:
                    # Format: "Rating: ⭐ 3.9 5"
                    # Ekstrak angka dengan regex
                    import re
                    match = re.search(r'(\d+\.\d+)', rating)
                    if match:
                        return float(match.group(1))
                return None
            except Exception as e:
                print(f"Error converting price: {e}")
                return None
        df_transformed['Rating'] = df_transformed['Rating'].apply(clean_rating)

        # 3. Extract just the number
        def extract_colors_count(colors):
                try:
                    if "Colors" in colors:
                        # Format: "3 Colors"
                        return int(colors.split()[0])
                    return None
                except Exception as e:
                    print(f"Error converting price: {e}")
                    return None
                
        df_transformed['Colors'] = df_transformed['Colors'].apply(extract_colors_count)

        # 4. Clean Size column 
        def clean_size(size):
            try:
                if "Size: " in size:
                    return size.replace("Size: ", "").strip()
                return size
            except Exception as e:
                print(f"Error converting price: {e}")
                return None
            
        
        df_transformed['Size'] = df_transformed['Size'].apply(clean_size)

        
        # 5. Clean Gender column (remove "Gender: " prefix)
        def clean_gender(gender):
            try:
                if "Gender: " in gender:
                    return gender.replace("Gender: ", "").strip()
                return gender
            except Exception as e:
                print(f"Error converting price: {e}")
                return None
        
        df_transformed['Gender'] = df_transformed['Gender'].apply(clean_gender)
    

        # 6. Remove duplicate rows
        df_transformed = df_transformed.drop_duplicates()

        # 7. Filter out rows with invalid or unwanted values
        df_transformed = df_transformed[df_transformed['Title'] != "Unknown Product"]

        
        return df_transformed
    
    except Exception as e:
        print(f"Error during transformation: {e}")
        return df

if __name__ == "__main__":
    # Import pandas dan buat contoh data untuk testing
    import pandas as pd
    
    # Buat contoh dataframe sederhana untuk test
    test_data = {
        'Title': ['Product A', 'Unknown Product'],
        'Price': ['$20', 'Price Unavailable'],
        'Rating': ['4.5 / 5', 'Invalid Rating'],
        'Colors': ['3 Colors', '1 Colors'],
        'Size': ['Size: M', 'Size: L'],
        'Gender': ['Gender: Men', 'Gender: Women']
    }
    df = pd.DataFrame(test_data)
    
    # Test transformasi
    transformed_df = transform_data(df)
    print(transformed_df.head())