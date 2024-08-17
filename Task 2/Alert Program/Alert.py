import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess the data
def setting_up_data(file: str):
    df = pd.read_csv(file)

    # Standardize the column with number of transactions
    df.rename(columns={df.columns[2]: 'transactions_count'}, inplace=True)

    df_pivot = df.pivot_table(index='time', columns='status', values='transactions_count', fill_value=0)

    # Reorder the columns from df_pivot
    column_order = ['processing', 'approved', 'refunded', 'denied', 'backend_reversed',
                    'reversed', 'failed']
    df_pivot = df_pivot[column_order]

    return df, df_pivot

# Create graph with real time data
def transactions_graph(df: pd.DataFrame, df_pivot: pd.DataFrame):
    # Obtaining total transactions
    df_totals = df.groupby('time')['transactions_count'].sum().reset_index()
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

    # Creating figure with two subplots stacked vertically
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 8), sharex=True)

    # Plotting line graph on first supblot (top)
    ax1.plot(df_totals['time'], df_totals['transactions_count'], label="Total Transactions")
    ax1.set_ylim(bottom=0)
    ax1.set_ylabel("# of Transactions")
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Only consider "problematic" status for second subplot (bottom)
    df_pivot_filtered = df_pivot_percentage.filter(regex='failed|reversed|denied')

    # Define custom colors for each stack of second subplot (bottom)
    # Blue, Purple, Orange, Red
    custom_colors = ["#3A7EB5", "#A020F0", "#FF9800", "#F44336"]

    # Plotting bar graph on second supblot (bottom)
    df_pivot_filtered.plot(kind='bar', stacked=True, ax=ax2, alpha=0.7, width=0.8, color=custom_colors)
    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Not Approved Transactions as\n% of Total Transactions")
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax2.tick_params(axis='y')

    # Configuring xlabels
    ax2.set_xlabel("Time")
    ax2.set_xticks(df_totals['time'][::90])

    # Adjusting overall graph
    fig.suptitle('Transactions Over Time')
    plt.subplots_adjust(right=0.80)

    plt.show()

# understand rejection pattern/treshold

# determine alert method and conditions

# report anomalies


if __name__ == "__main__":

    transaction_files = ["transactions_1.csv"]
    for file in transaction_files:
        # Read transactions data and store in variables
        df, df_pivot = setting_up_data(file)

    #transactions_graph(df, df_pivot)
