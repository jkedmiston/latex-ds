# Latex-DS
Python based generator for LaTeX docs/reports. 

# Installation
## Docker
* Build image, run script and save to folder
* `docker build -t myimage .`
* `docker run -v ${PWD}/examples:/app/examples -it myimage python examples/example1.py`

## Anaconda
Or, if you have `pdflatex` installed in your `PATH`, you can just do the standard
* `pip install -r requirements.txt`
* `export PYTHONPATH=/path/to/this/repo`
* `python /path/to/this/repo/examples/example1.py`
For Mac computers this can be facilitated by the mactex package, `brew cask install mactex`, for Ubuntu `apt-get install texlive-latex-base`, though I usually just get `texlive-latex-extra`. 

In most cases this setup process would by
* `cd latex-ds`
* `export PYTHONPATH=$PWD`
* `python examples/example1.py`
* Open pdf in your editor, `open examples/example1.pdf`.

# Notes
* On Ubuntu 16, I needed to do some steps to set up Docker https://askubuntu.com/a/477554
