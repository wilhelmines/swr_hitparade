import marimo

__generated_with = "0.9.1"
app = marimo.App(width="full")


@app.cell
def __():
    import pandas as pd
    import altair as alt
    return alt, pd


@app.cell
def __(pd):
    df = pd.read_csv('data_aggregation/data/swr_hitparade_2022_2024_spotify_data.csv')
    return (df,)


@app.cell
def __(df):
    df_melted = df.melt(id_vars=['Artist', 'Title'], 
                        value_vars=['Rank_2022', 'Rank_2023', 'Rank_2024'],
                        var_name='Year', value_name='Rank')
    return (df_melted,)


@app.cell
def __(df_melted):
    df_melted['Year'] = df_melted['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
    df_counts = df_melted.dropna().groupby(['Artist', 'Year']).size().reset_index(name='Appearances')
    return (df_counts,)


@app.cell
def __(df_counts):
    artist_totals = df_counts.groupby('Artist')['Appearances'].sum().astype(int).reset_index()
    artist_totals = artist_totals.rename(columns={'Appearances': 'TotalAppearances'})
    df_counts_merged = df_counts.merge(artist_totals, on='Artist')
    return artist_totals, df_counts_merged


@app.cell
def __(alt, df_counts_merged):
    chart_bar = alt.Chart(df_counts_merged).mark_bar().encode(
        y=alt.Y('Artist:N', sort='-x', title=''),  # Sorting by total appearances
        x=alt.X('sum(Appearances):Q', title='Anzahl der Songs'),
        color=alt.Color('Year:N', scale=alt.Scale(scheme='tableau20'), title='Year'),
        tooltip=[alt.Tooltip('Artist:N'),
                 alt.Tooltip('Year:N'),
                 alt.Tooltip('Appearances:Q'),
                 alt.Tooltip('TotalAppearances:Q')],  # Specifying the type here
    ).properties(
        width=800,
        height=9000,
        title=alt.Title(
            "Absolute Häufigkeit der Songs in der SWR1-Hitparade, gruppiert nach Künstler*innen",
            subtitle="Erstellt von github.com/wilhelmines, Datenquelle: swr-vote.de"
        ),
        padding={"left": 0, "top": 15, "right": 15, "bottom": 15},
    )
    return (chart_bar,)


@app.cell
def __(chart_bar):
    chart_bar
    return


@app.cell
def __(alt, df):
    df_chart_line = df.rename(columns={'Rank_2022': '2022', 'Rank_2023': '2023', 'Rank_2024': '2024'})

    chart_line = alt.Chart(df_chart_line).transform_window(
        index='count()'
    ).transform_fold(
        ['2022', '2023', '2024']
    ).mark_line(point=True).encode(
        x=alt.X(
            'key:O',
            title='Year',
            scale=alt.Scale(
                padding=0.05
            )
        ),
        y= alt.Y(
            'value:Q',
            title='Rank',
            scale=alt.Scale(domain = (0, 1072))
        ),
        color=alt.Color(
            'Title:N',
            legend=alt.Legend(
                title='Song',
                symbolLimit=0,
            )
        ),
        detail='index:N',
        opacity=alt.value(0.6),
        tooltip=[alt.Tooltip('Artist:N'),
                 alt.Tooltip('Title:N'),
                 alt.Tooltip('value:Q')],
    ).properties(
        height=19275,
        width=1700,
        title=alt.Title(
            "Platzierungen der Songs in der SWR1-Hitparade",
            subtitle="Erstellt von github.com/wilhelmines, Datenquelle: swr-vote.de"
        ),
        padding={"left": 0, "top": 15, "right": 15, "bottom": 15})
    return chart_line, df_chart_line


@app.cell
def __(chart_line):
    chart_line
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
