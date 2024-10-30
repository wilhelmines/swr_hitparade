import marimo

__generated_with = "0.9.1"
app = marimo.App(width="medium")


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
def __(data):
    # Creating the Marimo selector for year
    data_long = data.melt(id_vars='Spotify Duration (ms)', 
                          value_vars=['Rank_2022', 'Rank_2023', 'Rank_2024'],
                          var_name='Rank Year', 
                          value_name='Rank')
    return (data_long,)


@app.cell
def __(alt):
    brush = alt.selection_interval(encodings=["x"])
    return (brush,)


@app.cell
def __(alt, brush, data_long, mo):
    #Altair chart
    chart = alt.Chart(data_long).mark_circle().encode(
        x=alt.X('Rank:Q', title='Rank'),
        y=alt.Y('Spotify Duration (ms):Q', title='Duration (seconds)', 
                scale=alt.Scale(zero=False),
                axis=alt.Axis(format='.1f')),
        color='Rank Year:N',
        tooltip=['Rank Year:N', 'Rank', 'Spotify Duration (ms)']
    ).transform_calculate(
        # Convert duration to seconds
        duration_seconds="datum['Spotify Duration (ms)'] / 1000"
    ).encode(
        y='duration_seconds:Q'
    ).add_params(brush)

    # marimo chart
    chart = mo.ui.altair_chart(chart)
    return (chart,)


@app.cell
def __(chart):
    chart
    return


app._unparsable_cell(
    r"""
    pip install \"vegafusion[embed]>=1.4.0\"
    """,
    name="__"
)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
