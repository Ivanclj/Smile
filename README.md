# Example project repository

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv`](#with-virtualenv)
    + [With `conda`](#with-conda)
    + [With `make`](#with-make)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
  * [5. Interact with the application](#5-interact-with-the-application)
- [Creating the trained model object with Make](#creating-the-trained-model-object-with-make)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

**Vision**: To enable animals everywhere to enjoy music just for them. 

**Mission**: Enable users to add songs that they like and produce new song recommendations based on their entries.

**Success criteria**: Users play 80% of recommended songs more than once. 


_Note_: Project charters should actually be more detailed than this! But this is where the charter belongs.  

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. See bottom of README for exploratory data analysis environment setup. 

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n pennylane python=3.7
conda activate pennylane
pip install -r requirements.txt

```

#### With `make`

You can run the command:
 ```bash
 make venv
 ``` 
 to create the virtual environment. You will still need to activate the environment afterwards because it runs the command to create the environment from a separate terminal. 

### 2. Configure Flask app 

`app/config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3002  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/tracks.db'  # URI for database that contains tracks

```

* You will need to update the `PORT` configuration to your assigned port when deploying on the MSiA server (reach out to the instructors if you have not been assigned one)

* The configuration currently says to save the database to a temporary location as it is just for testing. However, if you are not on your local machine, you may have issues with this location and should change it to a location within your home directory, where you have full permissions. To change it to saving in the data directory within this repository, run the Python code from this directory and change the `config.py` to say:

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/tracksB.db'
```

The three `///` denote that it is a relative path to where the code is being run (which is from `src/add_songs.py`). 

You can also define the absolute path with four `////`:

```python
SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/chloemawer/repos/MSIA423-example-project-repo-2019/data/tracks.db'
```

### 3. Initialize the database 

To create the database in the location configured in `config.py` with one initial song, run: 

`python run.py create --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`

To add additional songs:

`python run.py ingest --artist=<ARTIST> --title=<TITLE> --album=<ALBUM>`


### 4. Run the application 
 
 ```bash
 python run.py app
 ```


You can also use `make` by running:

```bash
make app
```

### 5. Interact with the application 

a. On your computer - go to [http://127.0.0.1:3000/](http://127.0.0.1:3000/) to interact with the current version of the app. 

b. On the MSiA server:  when deploying the web app on the MSiA server you will need to run the following command **on your computer** (not on the server) before you can see the web app (you might be prompted for you NUIT password):

```bash
ssh -L $USER_PORT:127.0.0.1:$USER_PORT $NUIT_USER@msia423.analytics.northwestern.edu
```

* Replace the variable `$USER_PORT` with your assigned MSiA server port (reach out to the instructors if you have not been assigned one) and
`$NUIT_USER` with your NUIT username. An example: `ssh -L 3000:127.0.0.1:9000 fai3458@msia423.analytics.northwestern.edu` (We use the same port number for both the remote and local ports for convenience)

* Go to `http:127.0.0.1:$USER_PORT` to interact with the app. 


## Creating the trained model object with Make

From the command line, run: 

```bash
make trained-model
```

Running `make trained-model` is the same as running `make models/example.pkl` - the *PHONY* directive just allows for an easier command that creates a potentially long file name. 

When running either `make trained-model` or `make models/example.pkl`, if the file does not exist, it will run the command defined under `models/example.pkl` to create it:

```bash
python run.py train_model --config=config/test_model_config.yml --input=data/features/example-features.csv --output=models/example-model.pkl
```

If `models/example.pkl` does exist but any of the files it depends on (`data/sample/music_data_combined.csv`, `src/generate_features.py`, and `config/test_model_config.yml`) have changed since `models/example-model.pkl` was created, it will run the command again to recreate the model file. 

If `data/features/example-features.csv` doesn't exist when calling `make trained-model` or if it has changed since its dependencies were last changed, it will also create `data/features/example-features.csv` using the command defined for it.  

Therefore, the first time you run `make trained-model`, it will create the features file and then the trained model object because neither exists. 

If you change the configurations file, the code files, or the raw data file, it will recreate the trained model object in subsequent runs. 

It is suggested that you version any models and their corresponding configuration files between changes of the configuration YAML or any other dependencies. 


## Making predictions 

From the command line, run: 

```bash
python pennylane.py --config=<path-to-config> --input=<path-to-data-to-score> --output=<path-to-save-data>
```

or to make predictions with example data inputs and test configuration file: 

```bash
make predictions
```

## Testing 

Run `pytest` from the command line in the main project repository. 


Tests exist in `test/test_helpers.py`

You can also run the command: 

```bash
make test
```

<!--stackedit_data:
eyJoaXN0b3J5IjpbNjI5NjI2NTE2XX0=
-->