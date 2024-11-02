import pandas as pd

def load_data(filename):
    # Load data from a CSV file
    data = pd.read_csv(filename)
    # Remove leading/trailing spaces from column names
    data.columns = data.columns.str.strip()
    
    # Check what columns are loaded
    print("Loaded columns:", data.columns.tolist())  # Print columns for debugging

    # Simple preprocessing: drop missing values
    data = data.dropna()
    return data

if __name__ == "__main__":
    filename = 'C:/ecom/ecom_project/ecom_project/project/sales_data.csv'  # Adjust the path as needed
    data = load_data(filename)
    print(data.head())  # Display the first few rows of the loaded data
