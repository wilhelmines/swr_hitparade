import marimo

__generated_with = "0.9.1"
app = marimo.App(width="full")


@app.cell
def __():
    import pandas as pd
    import altair as alt
    import plotly.express as px
    return alt, pd, px


@app.cell
def __(pd):
    df = pd.read_csv('data_aggregation/data/swr_hitparade_raw.csv')
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
        x=alt.X('sum(Appearances):Q', title='Number of Appearances'),
        color=alt.Color('Year:N', scale=alt.Scale(scheme='tableau20'), title='Year'),
        tooltip=[alt.Tooltip('Artist:N'),
                 alt.Tooltip('Year:N'),
                 alt.Tooltip('Appearances:Q'),
                 alt.Tooltip('TotalAppearances:Q')],  # Specifying the type here
    ).properties(
        width=800,
        height=9000,
        title="Absolute Häufigkeit der Songs, gruppiert nach Künstler*innen, in der SWR1-Hitparade",
        padding={"left": 0, "top": 15, "right": 15, "bottom": 15}
    )
    return (chart_bar,)


@app.cell
def __(chart_bar):
    chart_bar
    return


@app.cell
def __(df):
    df_2 = df[(df['Rank_2022'] <= 100) | (df['Rank_2023'] <= 100) | (df['Rank_2024'] <= 100)]
    return (df_2,)


@app.cell
def __(alt, df):
    chart_line = alt.Chart(df).transform_window(
        index='count()'
    ).transform_fold(
        ['Rank_2022', 'Rank_2023', 'Rank_2024']
    ).mark_line().encode(
        x='key:N',
        y='value:Q',
        color='Spotify_Duration_(ms):N',
        detail='index:N',
        opacity=alt.value(0.5)
    ).properties(
        height=6000,
        width=1700,
        title="Platzierungen der Songs in der SWR-Hitparade",
        padding={"left": 0, "top": 15, "right": 15, "bottom": 15})
    return (chart_line,)


@app.cell
def __(chart_line):
    chart_line
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
