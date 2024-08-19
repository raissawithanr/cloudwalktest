# CloudWalk Monitoring Analyst Test

This repository contains the solutions for the Monitoring Analyst Test. It is divided into two tasks: anomaly detection in checkout data (Task 1) and implementation of a real-time transaction monitoring system (Task 2).

## Repository Structure

- **cloudwalktest/**
  - **Task 1/**
    - `SQL_Query.sql`: SQL query used for Task 1.
    - `README.md`: Documentation explaining Task 1.
  - **Task 2/**
    - `monitoring_script.py`: Python script for the real-time monitoring system.
    - `README.md`: Documentation explaining Task 2.
  - `README.md`: Overview of the entire project.


## Overview

This repository includes two main tasks:

1. **Task 1:** Analyzing checkout data to identify potential anomaly behavior.
2. **Task 2:** Implementing a real-time transaction monitoring and alert system using Python.

### Task 1: Checkout Data Anomaly Detection

In this task, an SQL query is used to analyze checkout data to identify anomalies. The query compares checkout data across different time periods (e.g., today, yesterday, same day last week, averages) to detect irregular patterns.

- **SQL Script:** `SQL_Query.sql`
- **Documentation:** The `README.txt` in the Task 1 folder explains the SQL script, its purpose, and how to execute it.

### Task 2: Real-Time Transaction Monitoring System

This task involves building a Python-based system that monitors transactions in real-time, detects anomalies using both threshold-based filtering and the Isolation Forest algorithm, and generates alerts when problematic transactions exceed defined thresholds.

- **Python Script:** `monitoring_script.py`
- **Documentation:** The `README.txt` in the Task 2 folder provides detailed instructions on how to use the Python script, the functions it includes, and how to customize the system.

## Requirements

### General Requirements
- MySQL 8.0 or higher for running the SQL queries in Task 1.
- A working environment with Python 3.7 or higher for Task 2.


### Python-Specific Requirements (Task 2)
- Python packages:
  - `pandas`
  - `matplotlib`
  - `scikit-learn`
 
## Instructions

### Task 1: Running the SQL Query

1. **Prepare the Database:**
   - Ensure that the MySQL database is set up and that the `checkout_1` and `checkout_2` tables are populated with the relevant data.

2. **Execute the SQL Query:**
   - Run the SQL query provided in `SQL_Query.sql` to analyze the checkout data.

3. **Review the Results:**
   - The query will produce results that highlight any anomalies or irregular patterns in the checkout data.

For more detailed instructions, refer to the `README.md` file in the Task 1 directory.

### Task 2: Running the Python Script

1. **Setup:**
   - Modify the `transaction_files` list in the `__main__` section of the `monitoring_script.py` to include paths to your CSV files.

2. **Run the Script:**
   - Execute the script using the following command:
     ```bash
     python monitoring_script.py
     ```

3. **Output:**
   - The script processes each file, generates alerts for any issues detected, and visualizes the results with graphs.

For more detailed instructions, refer to the `README.md` file in the Task 2 directory.

## Customization

- **Task 1:** The SQL query can be modified to adapt to different data structures or additional analysis requirements.
- **Task 2:**
  - The `transaction_files` list can be modified to include the paths to your transaction files.
  - The threshold for alerts can be adjusted by modifying the `threshold` variable.
  - The sensitivity of the Isolation Forest model can be fine-tuned by adjusting the `contamination` parameter.

## Limitations

- **Task 1:**
  - The SQL script assumes a specific data structure. If your dataset varies, adjustments may be necessary.
- **Task 2:**
  - The Python script assumes that the third column in the CSV files represents the transaction count. Changes may be needed for different data formats.
  - The Isolation Forest model’s performance may vary depending on the dataset. Fine-tuning may be required for optimal results.
  - The threshold for flagging problematic transactions is currently fixed. If a dynamic or context-sensitive threshold is required, the code would need to be modified accordingly.

## Conclusion

This repository demonstrates the implementation of a real-world monitoring and anomaly detection system. The SQL and Python scripts provided can be customized and extended to fit various business needs related to data analysis and monitoring.
