# Latex-DS
Python based generator for latex docs.


# Docker
* On Ubuntu 16, needed to do some steps https://askubuntu.com/a/477554
* Build image, run script and save to folder
* `docker build -t myimage .`
* `docker run -v ${PWD}/examples:/app/examples -it myimage python examples/example1.py`

# Anaconda
Or, if you have pdflatex installed in your `PATH`, you can just do the standard
* `pip install -r requirements.txt`
* `export PYTHONPATH=/path/to/this/repo`
* `python /path/to/this/repo/examples/example1.py`
E.g. in most cases:
* `cd latex-ds`
* `export PYTHONPATH=$PWD`
* `python examples/example1.py`
