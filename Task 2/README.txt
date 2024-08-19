Transaction Anomaly Detection and Alert System
==============================================

This project implements a transaction anomaly detection and alert system using a combination of threshold-based filtering and machine learning (Isolation Forest). The system processes transaction data, detects potential issues, and generates alerts when the percentage of problematic transactions exceeds a defined threshold.

Overview
--------
This script reads transaction data from CSV files, identifies potential issues such as failed, reversed, or denied transactions, and generates alerts when these issues exceed a specified threshold. Additionally, the system uses the Isolation Forest algorithm to detect anomalies in the transaction data and visualize the results using graphs.

Features
--------
- Threshold-Based Alerts: Generates alerts when the percentage of problematic transactions exceeds a defined threshold.
- Anomaly Detection: Uses the Isolation Forest algorithm to detect anomalies in flagged transactions.
- Data Visualization: Provides graphs showing total transactions and the percentage of problematic transactions over time.

Requirements
------------
- Python 3.7 or higher
- Required Python packages:
  - pandas
  - matplotlib
  - scikit-learn

Usage
-----
1. Modify the `transaction_files` list in the `__main__` section to include the paths to your CSV files.

2. Run the script:

   python monitoring_script.py

3. The script will process each file, generate alerts for any issues detected, and visualize the results.

Functionality Details
---------------------
Functions:

- `setting_up_data(file_name: str) -> tuple[pd.DataFrame, pd.DataFrame]`:
  - Loads and preprocesses the transaction data.
  - Returns two DataFrames: the original transaction data and a pivoted summary by transaction status.

- `threshold_filtering(df_pivot: pd.DataFrame, threshold: int) -> pd.Index`:
  - Identifies time periods where the percentage of problematic transactions exceeds the specified threshold.
  - Returns an index of flagged time periods.

- `alert_above_normal(df: pd.DataFrame, flagged_times: pd.Index, threshold: int)`:
  - Analyzes flagged transactions and generates alerts if the percentage of failed, reversed, or denied transactions exceeds the threshold.

- `isolation_forest(df: pd.DataFrame, flagged_times: pd.Index) -> pd.DataFrame`:
  - Uses the Isolation Forest algorithm to detect anomalies in flagged transactions.
  - Returns a DataFrame containing detected anomalies.

- `report_anomalies(df_anomalies: pd.DataFrame)`:
  - Prints the detected anomalies.

- `transactions_graph(df_transactions: pd.DataFrame, df_transactions_pivot: pd.DataFrame)`:
  - Generates and displays graphs showing total transactions and the percentage of problematic transactions over time.

Customization
-------------
- Threshold: Adjust the `threshold` variable in the `__main__` section to change the sensitivity of the alert system.
- CSV File Paths: Modify the `transaction_files` list to include the paths to your transaction files.

Limitations
-----------
- The script currently assumes that the third column in the CSV file contains the transaction count. If your dataset has a different structure, you may need to adjust the column indexing.
- The Isolation Forest model may require fine-tuning for datasets with different characteristics.
- The threshold for flagging problematic transactions is currently fixed. If a dynamic or context-sensitive threshold is required, the code would need to be modified accordingly.
