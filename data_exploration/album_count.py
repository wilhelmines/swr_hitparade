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
def __(df):
    df_melted = df.melt(id_vars=['Artist', 'Title', 'Spotify_Album_Name'], 
                        value_vars=['Rank_2022', 'Rank_2023', 'Rank_2024'],
                        var_name='Year', value_name='Rank')
    return (df_melted,)


@app.cell
def __(df_melted):
    df_melted['Year'] = df_melted['Year'].astype(str).str.extract(r'(\d{4})').astype(int)
    df_counts = df_melted.dropna().groupby(['Spotify_Album_Name', 'Year']).size().reset_index(name='Appearances')
    return (df_counts,)


@app.cell
def __(df_counts):
    artist_totals = df_counts.groupby('Spotify_Album_Name')['Appearances'].sum().astype(int).reset_index()
    artist_totals = artist_totals.rename(columns={'Appearances': 'TotalAppearances'})
    df_counts_merged = df_counts.merge(artist_totals, on='Spotify_Album_Name')
    return artist_totals, df_counts_merged


@app.cell
def __(alt, df_counts_merged):
    chart_bar = alt.Chart(df_counts_merged).mark_bar().encode(
        y=alt.Y('Spotify_Album_Name:N', sort='-x', title=''),  # Sorting by total appearances
        x=alt.X('sum(Appearances):Q', title='Anzahl der Songs'),
        color=alt.Color('Year:N', scale=alt.Scale(scheme='tableau20'), title='Jahr'),
        tooltip=[alt.Tooltip('Spotify_Album_Name:N'),
                 alt.Tooltip('Year:N'),
                 alt.Tooltip('Appearances:Q'),
                 alt.Tooltip('TotalAppearances:Q')],  # Specifying the type here
    ).properties(
        width=800,
        height=16000,
        title=alt.Title(
            "Absolute Häufigkeit der Alben in der SWR1-Hitparade, gruppiert nach Künstler*innen",
            subtitle="Erstellt von github.com/wilhelmines, Datenquelle: swr-vote.de"
        ),
        padding={"left": 15, "top": 15, "right": 15, "bottom": 15},
    )
    return (chart_bar,)


@app.cell
def __(chart_bar):
    chart_bar
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
