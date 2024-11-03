import marimo

__generated_with = "0.9.1"
app = marimo.App(width="full")


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import altair as alt
    return alt, mo, pd


@app.cell
def __(pd):
    df = pd.read_csv('data_aggregation/data/swr_hitparade_2022_2024_spotify_data.csv')
    return (df,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
