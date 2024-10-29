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
    return (df_hitparade,)


@app.cell
def __(
    ColumnDataSource_1,
    HoverTool_1,
    df,
    df_hitparade,
    figure_1,
    pd,
    source,
):
    artists = df_hitparade['Artist']
    _df = df_hitparade
    appearances_2022 = df[df['Rank_2022'].notnull()]['Artist'].value_counts()
    appearances_2023 = df[df['Rank_2023'].notnull()]['Artist'].value_counts()
    combined_counts = pd.DataFrame({'Artist': appearances_2022.index.union(appearances_2023.index), 'Count_2022': appearances_2022.reindex(appearances_2022.index.union(appearances_2023.index), fill_value=0), 'Count_2023': appearances_2023.reindex(appearances_2022.index.union(appearances_2023.index), fill_value=0)}).fillna(0)
    combined_counts['Total_Count'] = combined_counts['Count_2022'] + combined_counts['Count_2023']
    combined_counts = combined_counts[['Total_Count', 'Artist']]
    combined_counts = combined_counts.sort_values(by='Total_Count', ascending=True)
    _source = ColumnDataSource_1(data=dict(artists=combined_counts['Artist'], counts=combined_counts['Total_Count']))
    _output_file('artist_counts_horizontal.html')
    bar_fig = figure_1(y_range=combined_counts['Artist'], title='Artist Appearances', x_axis_label='Appearances', y_axis_label='Artist', height=8000, width=1500, toolbar_location=None)
    bars = bar_fig.hbar(y='artists', right='counts', source=source, height=0.7, color='green', legend_label='Appearances')
    bar_fig.text(x='counts', y='artists', source=_source, text='counts', text_align='left', text_font_size='10pt', x_offset=5, y_offset=4)
    hover = HoverTool_1(renderers=[bars], tooltips=[('Artist', '@artists'), ('Appearances', '@counts')])
    bar_fig.add_tools(hover)
    bar_fig.yaxis.major_label_orientation = 'horizontal'
    bar_fig.yaxis.major_label_text_font_size = '10pt'
    bar_fig.legend.location = 'bottom_right'
    bar_fig.legend.orientation = 'horizontal'
    _show(bar_fig)
    _save(bar_fig)
    return (
        appearances_2022,
        appearances_2023,
        artists,
        bar_fig,
        bars,
        combined_counts,
        hover,
    )


@app.cell
def __(df_hitparade):
    df_hitparade[df_hitparade['Artist']=='Das Lumpenpack']
    return


@app.cell
def __(ColumnDataSource_2, df, df_hitparade, figure_2):
    from bokeh.models import ColumnDataSource
    from bokeh.plotting import figure, show
    _df = df_hitparade
    _source = ColumnDataSource_2(df)
    p = figure_2(x_range=('2022', '2023'), y_range=(0, 1070), x_axis_location='above', y_axis_label='Rank in SWR Hitparade')
    p.scatter(x='Artist', y='Rank_2022', source=_source, size=7)
    p.scatter(x='Artist', y='Rank_2023', source=_source, size=7)
    p.segment(x0='Artist', y0='Rank_2022', x1='Artists', y1='Rank_2023', source=_source, color='black')
    p.text(x='Artist', y='Rank_2022', text='Artists', source=_source, x_offset=7, y_offset=8, text_font_size='12px')
    p.xaxis.major_tick_line_color = None
    p.xaxis.major_tick_out = 0
    p.xaxis.axis_line_color = None
    p.yaxis.minor_tick_out = 0
    p.yaxis.major_tick_in = 0
    p.yaxis.ticker = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
    p.grid.grid_line_color = None
    p.outline_line_color = None
    _show(p)
    return ColumnDataSource, figure, p, show


if __name__ == "__main__":
    app.run()
