import marimo

__generated_with = "0.9.1"
app = marimo.App(width="medium")


@app.cell
def __():
    import pandas as pd
    return (pd,)


@app.cell
def __(pd):
    df_2022 = pd.read_csv('data_aggregation/data/swr_hitparade_2022_spotify_data.csv')
    df_2023 = pd.read_csv('data_aggregation/data/swr_hitparade_2023_spotify_data.csv')
    df_2024 = pd.read_csv('data_aggregation/data/swr_hitparade_2024.csv')
    df_2022_short = pd.read_csv('data_aggregation/data/swr_hitparade_2022.csv')
    df_2023_short = pd.read_csv('data_aggregation/data/swr_hitparade_2023.csv')
    df_2024_short = pd.read_csv('data_aggregation/data/swr_hitparade_2024.csv')
    return (
        df_2022,
        df_2022_short,
        df_2023,
        df_2023_short,
        df_2024,
        df_2024_short,
    )


@app.cell
def __(df_2022_short, df_2023_short, df_2024_short, pd):
    df_hitparade_raw = pd.merge(df_2022_short, df_2023_short, on=['Title', 'Artist'], how='outer')
    df_hitparade_raw = pd.merge(df_hitparade_raw, df_2024_short, on=['Title', 'Artist'], how='outer')
    # Define the desired order of columns
    desired_order_short = ['Artist', 'Title', 'Rank_2022', 'Rank_2023', 'Rank_2024'] + [col for col in df_hitparade_raw.columns if col not in ['Artist', 'Title', 'Rank_2022', 'Rank_2023', 'Rank_2024']]
    # Reorder the columns
    df_hitparade_raw = df_hitparade_raw[desired_order_short]
    df_hitparade_raw.to_csv('df_hitparade_raw.csv', index=False)
    return desired_order_short, df_hitparade_raw


@app.cell
def __(df_2022, df_2023, df_2024, pd):
    # Merge the two DataFrames on 'Title' and 'Artist' columns, keeping all columns from both files
    df_hitparade = pd.merge(df_2022, df_2023, on=['Title', 'Artist'], how='outer')
    df_hitparade = pd.merge(df_hitparade, df_2024, on=['Title', 'Artist'], how='outer')

    # Define the desired order of columns
    desired_order = ['Artist', 'Title', 'Rank_2022', 'Rank_2023', 'Rank_2024'] + [col for col in df_hitparade.columns if col not in ['Artist', 'Title', 'Rank_2022', 'Rank_2023', 'Rank_2024']]

    # Reorder the columns
    df_hitparade = df_hitparade[desired_order]

    # Save the reordered DataFrame into a new CSV file
    df_hitparade.to_csv('df_hitparade.csv', index=False)
    return desired_order, df_hitparade


if __name__ == "__main__":
    app.run()
