import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess the data
def setting_up_data(file: str):
    df = pd.read_csv(file)

    # Convert 'time' to string format
    df['time'] = df['time'].apply(lambda x: x.replace('h ', ':').strip())

    # Generate a complete list of time intervals (every minute of the day) as strings
    all_minutes = [time.strftime('%H:%M') for time in pd.date_range(start="00:00", end="23:59", freq="min")]

    # Set 'time' as the index
    df.set_index('time', inplace=True)

    # Pivot the data to get the status values by time, filling missing values with 0
    df_pivot = df.pivot_table(index='time', columns='status', values='f0_', fill_value=0)

    # Reindex to include all minutes of the day
    df_pivot = df_pivot.reindex(all_minutes, fill_value=0)

    return df, df_pivot

# Create graph with real time data
def transactions_graph(df: pd.DataFrame, df_pivot: pd.DataFrame):
    # Obtaining total transactions per time
    df_totals = df.groupby('time')['f0_'].sum().reset_index()
    df_pivot_percentage = df_pivot.div(df_pivot.sum(axis=1), axis=0) * 100

    # Creating figure with two subplots stacked vertically
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Plotting line graph on first supblot (top)
    ax1.plot(df_totals['time'], df_totals['f0_'], label="Total Transactions")
    ax1.set_ylabel("# of Transactions")
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left', bbox_to_anchor=(1, 1))

    # Plotting bar graph on second supblot (bottom)
    df_pivot_percentage.plot(kind='bar', stacked=True, ax=ax2, alpha=0.7, width=0.8)
    ax2.set_ylabel("% of Total Transactions")
    ax2.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax2.tick_params(axis='y')

    # Configuring xlabels
    ax2.set_xlabel("Time")
    ax2.set_xticks(df_totals['time'][::120])

    # Adjusting and showing graph
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

    transactions_graph(df, df_pivot)
