# atpdrawsapi
API which provides info on ATP draws.

## Updating Data

Draw data is which is added to the draws folder is uploaded to S3. Draw data should be downloaded as HTML from the ATP website, for instance [this page](https://www.atptour.com/en/scores/current/hong-kong/336/draws). There is a Lambda which listens for added files in S3 and updates the database with the information from the draws. Draws should generally be added before a tournament starts (i.e. once the draw becomes available) and after the tournament is over. The draws can also be uploaded while the tournament is going on. The database will only be updated if the draw data has changed since the last update.

## Python Instructions

### Installing Dependencies

First of all, you'll want to start a virtual environment for development:

```
# Note: vscode will automatically detect this
`python -m venv venv`
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

Installing CDK (you'll also want to run `npm install`):

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

To list the available stacks, you can run the `cdk list` command:

```
cdk list
```

To check the diff for CDK (this should be done prior to deploying to make sure the changes are as you'd expected them to be):

```
# confirm no unexpected differences
cdk diff
```

For deploying the Dynamo stack:

```
cdk deploy DynamoStack
```

For deploying the Lambda stack:

```
cdk deploy LambdaStack
```


## References

* Instructions on creating lambda layer: https://alannewcomer.medium.com/how-to-crawl-awss-whats-new-blog-with-a-python-lambda-function-and-slack-ddadbc4e127b