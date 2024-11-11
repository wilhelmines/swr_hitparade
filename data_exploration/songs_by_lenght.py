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
def __(data):
    # Creating the Marimo selector for year
    data_long = data.melt(id_vars=['Artist','Title','Spotify_Duration_(ms)'], 
                          value_vars=['Rank_2022', 'Rank_2023', 'Rank_2024'],
                          var_name='Rank Year', 
                          value_name='Rank')
    return (data_long,)


@app.cell
def __(alt, data_long, mo):
    #Altair chart
    chart = alt.Chart(data_long).mark_circle().encode(
        x=alt.X('Rank:Q', title='Rank',scale=alt.Scale(domain = (0, 1072))),
        y=alt.Y('Spotify_Duration_(ms):Q', title='Duration (seconds)', 
                scale=alt.Scale(zero=False),
                axis=alt.Axis(format='.1f')),
        color='Rank Year:N',
        tooltip=['Rank Year:N', 'Rank', 'Spotify_Duration_(ms)']
    ).transform_calculate(
        # Convert duration to seconds
        duration_seconds="datum['Spotify_Duration_(ms)'] / 1000"
    ).encode(
        y='duration_seconds:Q',
            tooltip=[alt.Tooltip('Artist:N'),
                alt.Tooltip('Title:N'),
                 alt.Tooltip('Rank:N'),]
    ).properties(
        width=1700,
        height=500,
        title = alt.Title("Songlänge und Rang in der SWR1-Hitparade für 2022-2024",
                          subtitle = "Erstellt von github.com/wilhelmines, Datenquelle: swr-vote.de"),
    )

    # marimo chart
    chart = mo.ui.altair_chart(chart)
    return (chart,)


@app.cell
def __(chart):
    chart
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
