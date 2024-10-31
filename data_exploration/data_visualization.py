import marimo

__generated_with = "0.9.1"
app = marimo.App()


@app.cell
def __():
    import pandas as pd
    return (pd,)


@app.cell
def __(pd):
    df_hitparade = pd.read_csv('data_aggregation/data/swr_hitparade_raw.csv')
    df = pd.read_csv('data_aggregation/data/swr_hitparade_raw.csv')
    return df, df_hitparade


@app.cell
def __(df_hitparade):
    df_hitparade[df_hitparade['Artist']=='Das Lumpenpack']
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
