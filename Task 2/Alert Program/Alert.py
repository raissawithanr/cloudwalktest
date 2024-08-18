import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder


# Load and preprocess the data
def setting_up_data(file_name: str) -> [pd.DataFrame, pd.DataFrame]:
    new_df = pd.read_csv(file_name)

    # Standardize the column name that has number of transactions
    new_df.rename(columns={new_df.columns[2]: 'transactions_count'}, inplace=True)

    new_df_pivot = new_df.pivot_table(index='time', columns='status', values='transactions_count',
                                      fill_value=0)

    # Reorder the columns from df_pivot
    column_order = ['processing', 'approved', 'refunded', 'denied', 'backend_reversed',
                    'reversed', 'failed']
    new_df_pivot = new_df_pivot[column_order]

    return new_df, new_df_pivot


# Determine threshold to filter "problematic" transactions


# Filter transactions times that exceeds determined threshold of "problematic" transactions
def threshold_filtering(df_pivot: pd.DataFrame, threshold: int) -> pd.Index:
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100
    df_pivot_perc_filtered = df_pivot_percentage.filter(regex='failed|reversed|denied')

    # Calculate the percentage of "problematic" transactions per minute
    problematic_percentage = df_pivot_perc_filtered.sum(axis=1)

    # Flag times when the percentage of "problematic" transactions exceeds the threshold
    flagged_times = problematic_percentage[problematic_percentage > threshold].index

    return flagged_times


# Use of Isolation Forest algorithm to determine which transactions are anomalies
def isolation_forest(df: pd.DataFrame, flagged_times: pd.Index) -> pd.DataFrame:
    # Add column with percentage of total transactions by that row
    df['total_per_time'] = df.groupby('time')['transactions_count'].transform('sum')
    df['transaction_percentage'] = (df['transactions_count'] / df['total_per_time']) * 100
    df.drop(columns=['total_per_time'], inplace=True)

    # Filter the data to only include problematic transactions and flagged times
    df_filtered = df[df['status'].str.contains('failed|reversed|denied', regex=True)]
    flagged_data = df_filtered[df_filtered['time'].isin(flagged_times)].copy()

    # As Isolation Forest model just takes numerical features, one-hot encode the 'status' column
    encoder = OneHotEncoder(sparse_output=False)
    status_encoded = encoder.fit_transform(flagged_data[['status']])
    status_encoded_df = pd.DataFrame(status_encoded,
                                     columns=encoder.get_feature_names_out(['status']),
                                     index=flagged_data.index)

    # Combine encoded features with the other features
    features = pd.concat([flagged_data[['transactions_count', 'transaction_percentage']],
                          status_encoded_df], axis=1)

    # Train an Isolation Forest model to detect anomalies
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(features)

    # Predict anomalies
    flagged_data.loc[:, 'anomaly'] = model.predict(features)
    anomalies = flagged_data[flagged_data['anomaly'] == -1].copy()
    anomalies.drop(columns=['transaction_percentage'], inplace=True)

    return anomalies


# Report and alert anomalies
def report_anomalies(df_anomalies: pd.DataFrame):
    print("Anomalies Detected:")
    print(df_anomalies)


# Create graphs of total transactions and percentage of "problematic" transactions
def transactions_graph(df_transactions: pd.DataFrame, df_transactions_pivot: pd.DataFrame):
    # Obtain total transactions
    df_totals = df_transactions.groupby('time')['transactions_count'].sum().reset_index()
    df_pivot_percentage = df_transactions_pivot.div(df_transactions_pivot.sum(axis=1), axis=0) * 100

    # Create figure with two subplots stacked vertically
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

    # Plot line graph on first supblot (top)
    ax1.plot(df_totals['time'], df_totals['transactions_count'], label="Total Transactions")
    ax1.set_ylim(bottom=0)
    ax1.set_ylabel("# of Transactions")
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Only consider "problematic" status for second subplot (bottom)
    df_pivot_perc_filtered = df_pivot_percentage.filter(regex='failed|reversed|denied')

    # Define custom colors for each stack of second subplot (bottom)
    # Blue, Purple, Orange, Red
    custom_colors = ["#3A7EB5", "#A020F0", "#FF9800", "#F44336"]

    # Plot bar graph on second supblot (bottom)
    df_pivot_perc_filtered.plot(kind='bar', stacked=True, ax=ax2, alpha=0.7, width=0.8,
                                color=custom_colors)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Not Approved Transactions as\n% of Total Transactions")
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax2.tick_params(axis='y')

    # Configure xlabels
    ax2.set_xlabel("Time")
    ax2.set_xticks(df_totals['time'][::90])

    # Adjust overall graph
    fig.suptitle('Transactions Over Time')
    plt.subplots_adjust(right=0.80)

    plt.show()


if __name__ == "__main__":
    transaction_files = ["transactions_1.csv"]

    for file in transaction_files:
        # Read transactions data and store in variables
        df, df_pivot = setting_up_data(file)

        # Determine threshold for acceptable quantity of "problematic" transactions per minute
        threshold = 5

        # Obtain which minutes have number of transactions that exceeds threshold
        flagged_times = threshold_filtering(df_pivot, threshold)

        # Use of machine learning to determine which flagged transactions are anomalies
        anomalies = isolation_forest(df, flagged_times)

        # Report anomalies
        report_anomalies(anomalies)

        # Graph data transactions
        transactions_graph(df, df_pivot)
