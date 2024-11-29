# **ETH Blockchain Data Analytics Project**

## **Project Overview**  
This is my first created end to end project aiming to showcase the data skills I am practicing in the field of high interest to me. The project analyzes Ethereum blockchain transactions, providing insights into transaction values, address activity, and block performance. The process includes data cleaning, feature engineering, querying with SQL, and visualization using Tableau.

---

## **Ethereum Transactions Dataset Overview**


The dataset used for this project, titled Ethereum Transactions, was sourced from [Kaggle](https://www.kaggle.com/datasets/blessontomjoseph/ethereum-transactions?resource=download&select=eth_transactions.csv). It captures a comprehensive snapshot of Ethereum blockchain activity over a three-hour period on December 4, 2022. The dataset includes detailed information on transactions, such as sender and receiver addresses, transaction values, block numbers, and timestamps. This limited time frame provides a focused view of blockchain activity, allowing for targeted analysis of transaction patterns, participant behavior, and block characteristics within a condensed window of activity.

---
## **Data Preprocessing and Cleaning**

The dataset was cleaned and prepared using the following steps:

- **Loading the Dataset:**  
  The raw transaction data was loaded into a Pandas DataFrame for manipulation.

- **Removing Duplicates:**  
  Duplicate entries were identified and removed to ensure accuracy.

- **Handling Missing Values:**  
  - Replaced missing transaction values (`value` column) with `0`.  
  - Removed rows missing critical information (e.g., `from_address`, `to_address`, `block_number`, etc.).

- **Filtering Columns:**  
  Retained only essential columns for analysis:  
  - `from_address`, `to_address`, `hash`, `block_number`, `block_hash`, `block_timestamp`, `value`.

- **Saving Cleaned Data:**  
  The cleaned dataset was saved as:  
  `cleaned_ethereum_transactions.csv`.

---

## **Feature Engineering**

New features were created to enhance the dataset:

- **Wei to ETH Conversion:**  
  Transaction values were converted from Wei to ETH with dynamic precision for small and large values.

- **Transaction Value Categorization:**  
  Transactions were categorized into groups:
  - Categories: `0-0.001`, `1-10`, `100-1k`, `>40k`, etc.

- **Outlier Identification:**  
  Transactions exceeding 100 ETH were flagged as outliers.

- **Transaction Count Per Block:**  
  The total number of transactions in each block was calculated and added as a new column:  
  `Transactions Per Block`.

- **Time-Based Feature:**  
  Extracted the hour from `block_timestamp` to facilitate time-based analysis:  
  `Transaction Hour`.

---

## **SQL Querying**

A SQLite database (`ethereum.db`) was created for querying the cleaned dataset. Key queries included:

- **Top Senders by Transaction Count:**
    ```sql
    SELECT from_address
    FROM transactions
    GROUP BY from_address
    ORDER BY COUNT(*) DESC
    LIMIT 10;
    ```

- **Top Receivers by Transaction Count:**
    ```sql
    SELECT to_address
    FROM transactions
    GROUP BY to_address
    ORDER BY COUNT(*) DESC
    LIMIT 10;
    ```

- **Largest Transactions by Value:**
    ```sql
    SELECT hash
    FROM transactions
    ORDER BY value_in_eth DESC
    LIMIT 10;
    ```

- **Top Buyers and Sellers by Transaction Value:**  
  Identified the addresses with the highest cumulative ETH received and sent.

Results were added to the DataFrame as Boolean columns indicating the presence of addresses or transactions in the top lists.

---

## **Visualizations**

**To view the Tableau Visualizations clink [here](https://public.tableau.com/views/EthereumBlockchainActivityInsightsfromAddressesBlocksandTransactions/EthereumBlockchainActivityInsightsfromAddressesBlocksandTransactions?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**


The project insights were visualized in Tableau through the following visualizations:

- **Transaction Value Categorization:**  
  A bar chart displaying transaction counts across different value ranges.

- **Address Activity:**  
  Highlighted tables showing the top senders and receivers by transaction count.

- **Top Blocks Analysis:**  
  Tables revealing blocks with the most transactions and the highest ETH value transferred.

- **Transaction Clusters:**  
  A bubble chart representing clusters of transactions by value in ETH.

- **Time-Based Trends:**  
  A bar chart showing transaction counts and values over time.

---

## **Tableau Story Structure**

- **Story Flow:**  
  The Tableau story outlines a narrative covering:
  1. **Transaction Value Categorization:** Distributing transactions into value categories, showcasing the transaction types as well.
  2. **Distribution of transaction value and count over time:** Exploring how activity fluctuates every 20 minutes.
  3. **Identifying Outliers using Clusters:** Insights into distribution of large and small transactions.
  4. **Top 10 Senders and Receivers:** Identifying and exploring the most active addresses.
  5. **Top 10 blocks per block size and transaction count:** Comparing the largest blocks to understand their differences.
 
---

## **Conclusion**

This project showcases an analysis workflow for Ethereum blockchain transactions. Through data cleaning, feature engineering, SQL querying, and visualization, it prepares and structures the dataset so it is ready for exploring addresses,transactions and block activity. 

By identifying the categories of transaction values, it was shown that most of the transactions were non-monetary transactions, which was backed by the exploration of most active blocks later on. Key addresses, identified as outliers, that exchanged significant amounts of ETH value were further explored to obtain details into these transactions.


