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
            title='Jahr',
            scale=alt.Scale(
                padding=0.05
            )
        ),
        y= alt.Y(
            'value:Q',
            title='Rang',
            scale=alt.Scale(domain = (0, 1072))
        ),
        color=alt.Color(
            'Title:N',
            legend=alt.Legend(
                title='Titel',
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
            "Platzierungen der Songs in der SWR1-Hitparade für die Jahr 2022-2024",
            subtitle="Erstellt von github.com/wilhelmines, Datenquelle: swr-vote.de"
        ),
        padding={"left": 0, "top": 15, "right": 15, "bottom": 15})
    return chart_line, df_chart_line


@app.cell
def __(chart_line):
    chart_line
    return


@app.cell
def __(df):
    # Melt the data so we have a single "Rank" column
    rank_data = df.melt(id_vars=['Artist', 'Title', 'Spotify_Popularity'],
                          value_vars=['Rank_2022', 'Rank_2023', 'Rank_2024'],
                          var_name='Year', value_name='Rank')
    return (rank_data,)


@app.cell
def __(alt, df, rank_data):
    # Parameters for dropdown selection
    year_param = alt.param(
        name="year_param", bind=alt.binding_select(options=['Rank_2022', 'Rank_2023', 'Rank_2024'], name='Select Ranking Year:')
    )
    artist_param = alt.param(
        name="artist_param", bind=alt.binding_select(options=[None] + sorted(df['Artist'].unique().tolist()), name='Select Artist:')
    )

    # Base chart
    base = alt.Chart(rank_data).mark_circle().encode(
        x=alt.X('Rank:N', title='Ranking', sort='ascending', scale=alt.Scale(reverse=False),axis=alt.Axis(labelOverlap='parity', tickCount=10)),
        y=alt.Y('Spotify_Popularity:Q', title='Spotify Popularity', axis=alt.Axis(tickCount=10),scale=alt.Scale(domain = (0, 100))),
        color=alt.condition(
            alt.datum.Artist == artist_param, alt.value('red'), alt.value('steelblue')
        ),
        size=alt.condition(
            alt.datum.Artist == artist_param, alt.value(100), alt.value(30)
        ),
        tooltip=['Artist', 'Title', 'Year', 'Rank', 'Spotify_Popularity']
    ).add_params(
        year_param,
        artist_param
    ).transform_filter(
        (alt.datum.Year == year_param) & (alt.datum.Rank != None)  # Filters out null ranks for the selected year
    )

    base.properties(
        width=1600,
        height=800,
        padding={"left": 20, "top": 10, "right": 15, "bottom": 20},
        title=alt.Title(
            "Vergleich von 'Spotify Popularity' und Platzierungen der Songs in der SWR1-Hitparade",
            subtitle="Erstellt von github.com/wilhelmines, Datenquelle: swr-vote.de"
        ),
    )
    return artist_param, base, year_param


@app.cell
def __():
    #base.save('rank_vs_pop.html')
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
