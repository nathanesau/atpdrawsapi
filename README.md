# atpdrawsapi
API which provides info on ATP draws

## Python Instructions

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
pytest
```

To run a particular test you can do:

```
pytest test/test_parser.py
```

## AWS Instructions

Installing CDK:

```
npm install -g aws-cdk
```

For initial setup of cdk app, I've run the following command:

```
cdk init app --language typescript
```

For initial setup for your account, you'll need to run `cdk bootstrap`:

```
cdk bootstrap
```

To deploy the CDK changes:

```
# confirm no unexpected differences
cdk diff

# deploys the cloudformation changes
cdk deploy
```
