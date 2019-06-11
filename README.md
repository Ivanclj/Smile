# Smile
## Developer: Lingjun Chen
#### QA: Si(Angela) Chen
# Outline

<!-- toc -->

- [Project Charter](#project-charter)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Instructions on getting data and database](#instructions-on-getting-data-and-database-ready)
- [Running the application](#running-the-application)
  * [1. Set up environment](#1-set-up-environment)
    + [With `virtualenv` and `pip`](#with-virtualenv)
    + [With `conda`](#with-conda)
  * [Reproduce Model Development](#optional-reproduce-model-development)
  * [2. Configure Flask app](#2-configure-flask-app)
  * [3. Initialize the database](#3-initialize-the-database)
  * [4. Run the application](#4-run-the-application)
  * [5. Interact with the application](#5-interact-with-the-application)
- [Testing](#testing)


## Project Charter

**Vision**:  
This app would allows employees at Tech companies to find out whether they need to seek treatment for potential mental health issues. It also helps Tech companies to track the mental health of their employees and provide them with necessary assistance if needed

**Mission**:  
Help users to find out whether they need treatment for mental health problems by taking their input on a series of survey question and predict outcome for the user. It would also provides a report on what are the factors impact the user's result

**Success criteria**:  
1. Machine Learning metric: The model would be evaluated on misclassification rate of whether predicted the correct outcome. A misclassification rate of 10% or lower denotes success  
2. Business metric: A Click through rate of 70% to see the detailed report from the user end and a MAU of 1,000 would denote success

You can see the full charter at docs/ProjectCharter.md

## Repo structure 

```
├── README.md                         <- You are here

├── config                            <- Directory for yaml configuration files for feature generation, model training, evaluation, etc.
|   ├── config.yml                    <- Configuration file for files in src/
|
|   ├── flask_config.py               <- Configuration file for Flask app
|
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated as well as databases for the app
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
Also contains all docs for different functions of the app
│
├── models                            <- Trained model objects (TMOs)
│   ├── sample/   					  <- Folder that contains pickle file of the model
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│
├── src                               <- Source data for the project
│   ├── load_data.py         <- Script for downloading raw data from github to data folder. 
│   ├── upload_data.py                <- Script for uploading data files to S3 bucket. 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for training and scoring.
│   ├── train_model.py                <- Script for training a machine learning model.
│   ├── evaluate_model.py             <- Script for evaluating model performance.
│   ├── database.py                     <- Creates the data model for the database connected to the Flask app.
|
├── test                              <- Files necessary for running model tests (see documentation below) 
│   ├── test_load_data.py                       <- Script for running unit tests on src/load_data.py.
│
│   ├── test_generate_features.py.py                       <- Script for running unit tests on src/generate_features.py.py.
│
│   ├── test_train_model.py.py                       <- Script for running unit tests on src/train_model.py.
│
│   ├── test_evaluate_models.py                       <- Script for running unit tests on src/evaluate_models.py.
│

├── static/                           <- CSS, JS files that remain static
├── templates/                        <- HTML (or other code) that is templated and changes based on a set of inputs

├── app.py                            <- Flask wrapper for running the model 

├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Instructions on getting data and database ready

* See `docs/database.md` for detailed guidelines to run scripts for retrieving project data and setting database


## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. First, `cd path_to_repo`

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv Smile

source Smile/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n Smile python=3.6
conda activate Smile
pip install -r requirements.txt

```

### Reproduce Model Development

To reproduce the whole model development process locally using Makefile, run following from command line in the main project repository:

```bash
cd path_to_repo
make all
```

If want to run steps separately, you can run following lines under main project repository:

1. load_data

```bash
make load_data
or
python src/load_data.py --config config/config.yml --savecsv data/survey.csv

```

2. generate_features

```bash
make features
or
python src/generate_features.py --config config/config.yml --loadcsv data/survey.csv --savecsv data/survey_cleaned.csv

```
3. train_model

```bash
make trained-model
or
python src/train_model.py --config config/config.yml --loadcsv data/survey_cleaned.csv --savemodel models/sample/random_forest.pkl

```

4. evaluate_model

```bash
make evaluate-model
or
python src/evaluate_model.py --config config/config.yml --loadmodel models/sample/random_forest.pkl
```

### 2. Configure Flask app 

`config/config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
SQLALCHEMY_DATABASE_URI # URL for database that contains bank customers
PORT = 3000  # What port to expose app on 
HOST = "0.0.0.0" # Host IP for the app 
```

### 3. Upload data to S3 bucket
To upload data to a specfic S3 bucket, please make sure you have aws credentials configured. This can be checked by running 
```bash
vi ~/.aws/credentials
```
If have credentials set up, then run in the terminal

```bash

python src/upload_data.py --input_file_path FILE_PATH --bucket_name S3_BUCKET_NAME --output_file_path S3_OUTPUT_FILE_PATH

```
### 3. Initialize the database 

To create a database locally, run: 

Note: an empty folder named database under <path_to_main_repository>/data has to be created to save the db. For creating a database on RDS, please refer to docs/database.md.

```bash
make database

or 

python src/database.py
```


### 4. Run the application 
To set up environment variable SQLALCHEMY_DATABASE_URI (URL for database that contains bank customers) from command line in the main project repository:
 ```bash
 
 Run locally: export SQLALCHEMY_DATABASE_URI='sqlite:///data/user_predictions.db'
 Run on RDS: export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"
 ```

then
 ```bash
make app

or

python app.py
 ```

:bulb: Tip:
When encountering the following error:

    OSError: [Errno 8] Exec format error
Please add the following line at the very beginning of `app.py`:
```
#!/usr/bin/env python3
```

### 5. Interact with the application

Go to [http://0.0.0.0:3000/]( http://0.0.0.0:3000/) to interact with the current version of the app locally. 

## Testing 

Run `make test` from the command line in the main project repository. 


Tests exist in `test/`

### Works Cited

General HTML Templates, CSS, js credit to Colorlib https://colorlib.com/wp/template/ (Woodrox, Dup, Maxitechture) and W3Schools https://www.w3schools.com/howto/ (buttons, styles, error page)

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMwNTQ0NjcxXX0=
-->

<!--stackedit_data:
eyJoaXN0b3J5IjpbNTY2MTQyNjkxXX0=
-->