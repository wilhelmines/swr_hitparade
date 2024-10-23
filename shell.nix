{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.pandas
    python312Packages.beautifulsoup4
    python312Packages.requests
    python312Packages.jupyterlab
    python312Packages.sparqlwrapper
    python312Packages.spotipy
  ];

PYTHONPATH = "$PWD";  # Sets the current directory in the Python path

}