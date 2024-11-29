import pandas as pd

# Loading dataset
file_path = r"C:\Users\Dunja\Desktop\pythonProject1\blockchain_analytics\data\eth_transactions.csv"
df = pd.read_csv(file_path)
print(df.head()) # preview first few rows


# Removing duplicates
df = df.drop_duplicates()
print("Duplicates removed.")


# Handling missing Values
# 1. Replace missing values with a default
df['value'] = df['value'].fillna(0)
# 2. Drop rows with missing values in critical columns
df = df.dropna(subset=['from_address', 'to_address', 'hash', 'block_number', 'block_hash', 'block_timestamp', 'value'])
print("Rows with missing critical values removed.")


# Filtering unnecessary columns
df = df[['from_address', 'to_address', 'hash', 'block_number', 'block_hash', 'block_timestamp', 'value']]
print("Unnecessary columns removed.")


# Saving cleaned dataset
df.to_csv("C:/Users/Dunja/Desktop/pythonProject1/blockchain_analytics/data/cleaned_ethereum_transactions.csv", index=False)
print("Cleaned data saved to 'cleaned_ethereum_transactions.csv'.")


# #Visualization
# # Transforming and querying data using SQL
# from sqlalchemy import create_engine
# import pandas as pd
#
# # Load cleaned dataset
# df = pd.read_csv("C:/Users/Dunja/Desktop/pythonProject1/blockchain_analytics/data/cleaned_ethereum_transactions.csv")


#Updating the dataset
import pandas as pd
from sqlalchemy import create_engine

# Load the cleaned dataset
file_path = "C:/Users/Dunja/Desktop/pythonProject1/blockchain_analytics/data/cleaned_ethereum_transactions.csv"
df = pd.read_csv(file_path)

# Convert 'value' from Wei to ETH with dynamic precision
def format_eth(value):
    eth_value = value / 1e18
    if eth_value < 0.1:
        return round(eth_value, 4)  # More precision for small values
    else:
        return round(eth_value, 1)  # Standard precision for larger values

# Apply conversion to 'value' column and create a new 'value_in_eth' column
df['value_in_eth'] = df['value'].apply(format_eth)

# Function to categorize 'value_in_eth'
def categorize_value(eth_value):
    if eth_value == 0:
        return "Non-monetary interaction"
    elif 0 < eth_value <= 0.001:
        return "0-0.001"
    elif 0.001 < eth_value <= 0.01:
        return "0.001-0.01"
    elif 0.01 < eth_value <= 0.1:
        return "0.01-0.1"
    elif 0.1 < eth_value <= 1:
        return "0.1-1"
    elif 1 < eth_value <= 10:
        return "1-10"
    elif 10 < eth_value <= 100:
        return "10-100"
    elif 100 < eth_value <= 1000:
        return "100-1k"
    elif 1000 < eth_value <= 10000:
        return "1k-10k"
    elif 10000 < eth_value <= 20000:
        return "10k-20k"
    elif 20000 < eth_value <= 30000:
        return "20k-30k"
    elif 30000 < eth_value <= 40000:
        return "30k-40k"
    else:
        return "> 40k"

# Apply categorization
df['Value Category'] = df['value_in_eth'].apply(categorize_value)

# Identify outliers based on 'value_in_eth'
df['is_outlier'] = df['value_in_eth'].apply(lambda x: "Yes" if x > 100 else "No")

# Create SQLite database for analysis
engine = create_engine("sqlite:///ethereum.db")
df.to_sql("transactions", engine, if_exists="replace", index=False)

# SQL queries for top addresses and transactions
queries = {
    'Is Top Seller': """
        SELECT from_address
        FROM transactions
        GROUP BY from_address
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """,
    'Is Top Buyer': """
        SELECT to_address
        FROM transactions
        GROUP BY to_address
        ORDER BY COUNT(*) DESC
        LIMIT 10;
    """,
    'Is Largest Transaction': """
        SELECT hash
        FROM transactions
        ORDER BY value_in_eth DESC
        LIMIT 10;
    """,
    'Is Biggest Buyer': """
        SELECT to_address
        FROM transactions
        GROUP BY to_address
        ORDER BY SUM(value_in_eth) DESC
        LIMIT 10;
    """,
    'Is Biggest Seller': """
        SELECT from_address
        FROM transactions
        GROUP BY from_address
        ORDER BY SUM(value_in_eth) DESC
        LIMIT 10;
    """
}

# Execute queries and create boolean columns in DataFrame
for label, query in queries.items():
    result = pd.read_sql(query, engine)
    addresses_or_hashes = result.iloc[:, 0].tolist()
    column_name = f'{label}'
    df[column_name] = df['from_address'].isin(addresses_or_hashes) | df['to_address'].isin(addresses_or_hashes) | df['hash'].isin(addresses_or_hashes)

# Add transaction count per block
block_transaction_count = df.groupby('block_number').size().rename("Transactions Per Block")
df = df.merge(block_transaction_count, on='block_number')

# Add transaction hour for time-based analysis
df['Transaction Hour'] = pd.to_datetime(df['block_timestamp']).dt.hour

# Save the updated dataset
output_path = "C:/Users/Dunja/Desktop/pythonProject1/blockchain_analytics/data/updated_ethereum_transactions.csv"
df.to_csv(output_path, index=False)

print(f"Updated dataset saved to {output_path}.")


