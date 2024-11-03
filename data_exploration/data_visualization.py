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
        ...
        """
    )
    return


if __name__ == "__main__":
    app.run()
