def save_to_csv(df, file_path='products.csv'):
    """
    Save DataFrame to CSV file.
    """
    try:
        df.to_csv(file_path, index=False)
        print(f"Data successfully saved to {file_path}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False