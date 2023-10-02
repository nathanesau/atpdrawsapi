# atpdrawsapi
API which provides info on ATP draws

## Developer Instructions

### Installing Dependencies

First of all, you'll want to start a virtual environment for development:

```
# Note: vscode will automatically detect this
python -m venv venv
```

Once you've activated the virtual environment, install any dependency as usual:

```
# installs BeautifulSoup
pip install bs4
```

If you want to write the installed packages to a file you can do this:

```
pip freeze > requirements.txt
```

If you want to install the requirements from this file on a new computer, install them as follows:

```
pip install -r requirements.txt
```

### Running Tests

You can run the unit tests as follows:

```
python -m unittest discover test
```

To run a particular test you can do:

```
python -m unittest test.test_parser
```
