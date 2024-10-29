{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    nodejs_22
    python312
    python312Packages.pandas
    python312Packages.beautifulsoup4
    python312Packages.requests
    python312Packages.sparqlwrapper
    python312Packages.spotipy
    python312Packages.bokeh
    python312Packages.marimo
    python312Packages.altair
  ];

PYTHONPATH = "$PWD";  # Sets the current directory in the Python path

}