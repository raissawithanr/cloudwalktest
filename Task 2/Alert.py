import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder


def setting_up_data(file_name: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load and preprocess the transaction data from a CSV file.

    Args:
        file_name (str): The path to the CSV file containing transaction data.

    Returns:
        tuple: A tuple containing two DataFrames:
            - new_df: preprocessed DataFrame with transaction data.
            - new_df_pivot: A pivoted DataFrame summarizing the transactions by status.
    """
    new_df = pd.read_csv(file_name)

    # Standardize the column name for the number of transactions
    new_df.rename(columns={new_df.columns[2]: 'transactions_count'}, inplace=True)

    # Pivot the data to organize transactions by status
    new_df_pivot = new_df.pivot_table(index='time', columns='status', values='transactions_count',
                                      fill_value=0)

    # Specify the desired order of columns
    desired_columns = ['processing', 'approved', 'refunded', 'denied', 'backend_reversed',
                       'reversed', 'failed']

    # Filter to only include columns that are present in the DataFrame
    column_order = [col for col in desired_columns if col in new_df_pivot.columns]

    # Reorder the columns in the pivoted DataFrame, keeping any additional columns at the end
    new_df_pivot = new_df_pivot[column_order
                                + [col for col in new_df_pivot.columns if col not in column_order]]

    return new_df, new_df_pivot


def threshold_filtering(df_pivot: pd.DataFrame, threshold: int) -> pd.Index:
    """
    Identify time periods where the percentage of problematic transactions exceeds a threshold.

    Args:
        df_pivot (pd.DataFrame): The pivoted DataFrame summarizing transactions by status.
        threshold (int): The threshold percentage for flagging problematic transactions.

    Returns:
        pd.Index: An index of time periods that exceed the specified threshold.
    """
    # Calculate the percentage of each status in each row
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

    # Filter for problematic statuses
    df_pivot_perc_filtered = df_pivot_percentage.filter(regex='failed|reversed|denied')

    # Calculate the total percentage of problematic transactions for each time period
    problematic_percentage = df_pivot_perc_filtered.sum(axis=1)

    # Get times when the percentage of problematic transactions exceeds the threshold
    filtered_times = problematic_percentage[problematic_percentage > threshold].index

    return filtered_times


def alert_above_normal (df: pd.DataFrame, flagged_times: pd.Index, threshold: int):
    """
    Analyze transactions during flagged times and generate alerts if the percentage
    of failed, reversed, or denied transactions exceeds the specified threshold.

    Args:
        df (pd.DataFrame): The original transaction data.
        flagged_times (pd.Index): An index of time periods that have been flagged for potential issues.
        threshold (int): The threshold percentage for generating alerts.

    Returns:
        None: This function prints alerts if the quantity of failed, reversed, or denied transactions
              exceeds the specified threshold.
    """
    # Filter for transactions occurring during the flagged times
    flagged_df = df[df['time'].isin(flagged_times)].copy()

    # Calculate the percentage of total transactions for each transaction during flagged times
    flagged_df['total_per_time'] = flagged_df.groupby('time')['transactions_count'].transform('sum')
    flagged_df['transaction_percentage'] = (flagged_df['transactions_count']
                                            / flagged_df['total_per_time']) * 100
    flagged_df.drop(columns=['total_per_time'], inplace=True)

    # Alert if quantity of failed transactions above normal
    df_failed = flagged_df[flagged_df['status'].str.contains('failed', regex=True)]
    df_failed = df_failed[df_failed['transaction_percentage'] >= threshold]
    if not df_failed.empty:
        print("There are more failed transactions than normal for those times:")
        print(df_failed['time'].tolist())

    # Alert for quantity of reversed transactions above normal
    df_reversed = flagged_df[flagged_df['status'].str.contains('reversed', regex=True)]
    df_reversed = df_reversed[df_reversed['transaction_percentage'] >= threshold]
    if not df_reversed.empty:
        print("There are more reversed transactions than normal for those times:")
        print(df_reversed['time'].tolist())

    # Alert for quantity of denied transactions above normal
    df_denied = flagged_df[flagged_df['status'].str.contains('denied', regex=True)]
    df_denied = df_denied[df_denied['transaction_percentage'] >= threshold]
    if not df_denied.empty:
        print("There are more denied transactions than normal for those times:")
        print(df_denied['time'].tolist())


def isolation_forest(df: pd.DataFrame, flagged_times: pd.Index) -> pd.DataFrame:
    """
    Use the Isolation Forest algorithm to detect anomalies in the flagged transactions.

    Args:
        df (pd.DataFrame): The original transaction data.
        flagged_times (pd.Index): An index of time periods that have been flagged.

    Returns:
        pd.DataFrame: A DataFrame containing the detected anomalies.
    """
    # Calculate the percentage of total transactions for each transaction
    df['total_per_time'] = df.groupby('time')['transactions_count'].transform('sum')
    df['transaction_percentage'] = (df['transactions_count'] / df['total_per_time']) * 100
    df.drop(columns=['total_per_time'], inplace=True)

    # Filter for problematic transactions and flagged times
    df_filtered = df[df['status'].str.contains('failed|reversed|denied', regex=True)]
    flagged_data = df_filtered[df_filtered['time'].isin(flagged_times)].copy()

    # One-hot encode the 'status' column for the Isolation Forest model
    encoder = OneHotEncoder(sparse_output=False)
    status_encoded = encoder.fit_transform(flagged_data[['status']])
    status_encoded_df = pd.DataFrame(status_encoded,
                                     columns=encoder.get_feature_names_out(['status']),
                                     index=flagged_data.index)

    # Combine encoded features with the other features
    features = pd.concat([flagged_data[['transactions_count', 'transaction_percentage']],
                          status_encoded_df], axis=1)

    # Train the Isolation Forest model to detect anomalies
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)

    # Predict anomalies and filter them
    flagged_data.loc[:, 'anomaly'] = model.predict(features)
    anomalies = flagged_data[flagged_data['anomaly'] == -1].copy()
    anomalies.drop(columns=['transaction_percentage'], inplace=True)

    return anomalies


def report_anomalies(df_anomalies: pd.DataFrame):
    """
    Report detected anomalies in the transaction data.

    Args:
        df_anomalies (pd.DataFrame): The DataFrame containing the detected anomalies.
    """
    print("\nAnomalies Detected:")
    print(df_anomalies)


def transactions_graph(df_transactions: pd.DataFrame, df_transactions_pivot: pd.DataFrame):
    """
    Create graphs of total number of transactions and the percentage of problematic transactions.

    Args:
        df_transactions (pd.DataFrame): The original transaction data.
        df_transactions_pivot (pd.DataFrame): The pivoted DataFrame summarizing transactions by status.
    """
    # Calculate total transactions for each time period
    df_totals = df_transactions.groupby('time')['transactions_count'].sum().reset_index()

    # Calculate the percentage of each status in each row
    df_pivot_percentage = df_transactions_pivot.div(df_transactions_pivot.sum(axis=1), axis=0) * 100

    # Create figure with two subplots stacked vertically
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

    # Plot a line graph of total transactions in the first subplot
    ax1.plot(df_totals['time'], df_totals['transactions_count'], label="Total Transactions")
    ax1.set_ylim(bottom=0)
    ax1.set_ylabel("# of Transactions")
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Filter for problematic statuses and define custom colors for the bar chart
    df_pivot_perc_filtered = df_pivot_percentage.filter(regex='failed|reversed|denied')
    custom_colors = ["#3A7EB5", "#A020F0", "#FF9800", "#F44336"]

    # Plot a stacked bar graph of problematic transactions in the second subplot
    df_pivot_perc_filtered.plot(kind='bar', stacked=True, ax=ax2, alpha=0.7, width=0.8,
                                color=custom_colors)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Problematic Transactions as\n% of Total Transactions")
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax2.tick_params(axis='y')

    # Configure x-axis labels
    ax2.set_xlabel("Time")
    ax2.set_xticks(df_totals['time'][::90])

    # Adjust the overall layout and display the graph
    fig.suptitle('Transactions Over Time')
    plt.subplots_adjust(right=0.80)

    plt.show()


if __name__ == "__main__":
    transaction_files = ["transactions_1.csv", "transactions_2.csv"]

    for file in transaction_files:
        # Load and preprocess the transaction data
        df, df_pivot = setting_up_data(file)

        # Define the threshold for flagging problematic transactions
        th = 5  # Represents 5% of total transactions

        # Identify the times that exceed the threshold for problematic transactions
        flagged_times = threshold_filtering(df_pivot, th)

        # Alert if number of problematic transactions per category is above 5% of total transactions
        alert_above_normal(df, flagged_times, th)

        # Detect anomalies using the Isolation Forest algorithm
        anomaly = isolation_forest(df, flagged_times)

        # Report detected anomalies
        if not anomaly.empty:
            report_anomalies(anomaly)

        # Visualize the transaction data
        transactions_graph(df, df_pivot)

        # Declare the end of the analysis for the current file
        print(f"\nAnalysis finalized for {file}\n")

    print("\nNo more alerts")
