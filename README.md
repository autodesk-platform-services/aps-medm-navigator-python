# MEDM CLI Tool

[![ver](https://img.shields.io/badge/language-python-orange.svg)](https://www.python.org/)
[![pep8](https://img.shields.io/badge/code%20style-pep8-blue.svg)](https://www.python.org/dev/peps/pep-0008/)

[![Stackoverflow](https://img.shields.io/badge/ask-stackoverflow-yellow.svg)](https://stackoverflow.com/questions/ask?tags=%5bautodesk-aps)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://opensource.org/licenses/MIT)

## Description
This is a Python sample, created in form of a CLI tool that helps to automate the process of reading collections, projects and assets using the M&E Data Model GraphQL API.

## Thumbnail
![thumbnail](./thumbnail.png)  

### Dependencies
* **Python**: Download [Python](https://www.python.org/downloads/). **It is required to use Python > 3.13**. 
* **APS Account**: Learn how to create an APS Account, activate subscription and create an app at [this tutorial](https://tutorials.autodesk.io/#create-an-account).

## Running locally
The Data Exchange calls requires 3-legged authenticated token. 
To simplify the sample and have only the minimum necessary code focused on M&E Data Model, the Authentication code is missing on purpose.
To run the sample, it is required to have the 3-legged authenticated token and set the `AUTH_TOKEN` var within [config.py](/config.py) file.

Within the project folder:

1. Create a virtual environment:
```commandline
    python -m venv venv
```

2. Activate the virtual environment:

For Windows:
```commandline
    venv\Scripts\activate.bat
```
For Linux/MacOS systems:
```commandline
    source venv/bin/activate
```

3. Install dependencies via pip:
```
    pip install -r requirements.txt
```

4. The app can be called by running
```
    python main.py
```

or you can set an alias:
```
alias medm="python3 main.py"
```

and call the app with further commands:

```commandline
medm getcollections
```

For the entire list of commands check [the documentation for the app](./docs.md).


## Knowing issues

- For brevity purpose, the error handling is missing from the code and almost all errors will default to `"ERROR: The Auth token expired"`


## License
These samples are licensed under the terms of the [MIT License](http://opensource.org/licenses/MIT). Please see the [LICENSE](LICENSE) file for full details.

### Authors

Denis Grigor ([denis.grigor@autodesk.com](denis.grigor@autodesk.com)), [APS Partner Development](http://aps.autodesk.com)

See more at [Developer Community Blog](https://aps.autodesk.com/blog).
