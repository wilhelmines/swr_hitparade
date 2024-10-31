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
    data = pd.read_csv('data_aggregation/data/swr_hitparade_2022_2024_spotify_data.csv')
    return (data,)


@app.cell
def __():
    # TODO Visual which shows the songs in correlation to their release date
    return


if __name__ == "__main__":
    app.run()
