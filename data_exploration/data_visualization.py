import marimo

__generated_with = "0.9.1"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    mo.md(
        r"""
        # Ideas for analytics:
        - large jumps
        - Mean/median rank of artist
        - Genre distribution
        - release date distribution
        - Usage of spotify parameter
            - Album/Single
            - Explicit
            - Popularity
        - distribution of artists with many songs
        - Tool where I can select an artist and it highlights their songs

        ...
        """
    )
    return


if __name__ == "__main__":
    app.run()
