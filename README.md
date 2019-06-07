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

├── test                              <- Files necessary for running model tests (see documentation below) 
│   ├── test.py                       <- Script for running unit tests on functions in src/.
│
├── static/                           <- CSS, JS files that remain static
├── templates/                        <- HTML (or other code) that is templated and changes based on a set of inputs
├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Instructions on getting data and database ready

* See `src/README.md` for detailed guidelines to run scripts for retrieving project data and setting database


## Running the application 
### 1. Set up environment 

The `requirements.txt` file contains the packages required to run the model code. An environment can be set up in two ways. First, `cd path_to_repo`

#### With `virtualenv`

```bash
pip install virtualenv

virtualenv pennylane

source pennylane/bin/activate

pip install -r requirements.txt

```
#### With `conda`

```bash
conda create -n tibank python=3.7
conda activate tibank
pip install -r requirements.txt
(optional): to solve Command 'pip' not found: conda install pip then pip install -r requirements.txt

```

### (Optional) Reproduce Model Development

To reproduce the whole model development process locally using Makefile, run following from command line in the main project repository:

```bash
export SQLALCHEMY_DATABASE_URI='sqlite:///data/database/churn_prediction.db'
make all
```

### 2. Configure Flask app 

`config.py` holds the configurations for the Flask app. It includes the following configurations:

```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
SQLALCHEMY_DATABASE_URI # URL for database that contains bank customers
PORT = 3002  # What port to expose app on - CHANGE TO 3000 if running on RDS
HOST = "127.0.0.1" # Host IP for the app - CHANGE TO "0.0.0.0" if running on RDS
```


### 3. Initialize the database 

To create a database in the local location configured in `config.py` with five initial customers, run: 

Note: an empty folder named database under <path_to_main_repository>/data has to be created to save the db. For creating a database on RDS, please refer to README.md in src/ folder.

```bash
cd path_to_repo/src
python models.py
```


### 4. Run the application 
To set up environment variable SQLALCHEMY_DATABASE_URI (URL for database that contains bank customers) from command line in the main project repository:
 ```bash
 cd path_to_repo
 Run locally: export SQLALCHEMY_DATABASE_URI='sqlite:///data/database/churn_prediction.db'
 Run on RDS: export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"
 ```

then
 ```bash
 python app.py
 ```

:bulb: Tip:
When encountering the following error:

    OSError: [Errno 8] Exec format error
Please add the following line at the very beginning of `app.py`:
```
#!/usr/bin/env python
```

### 5. Interact with the application

Go to [http://127.0.0.1:3002/]( http://127.0.0.1:3002/) to interact with the current version of the app locally. 

## Testing 

Run `make test` from the command line in the main project repository. 


Tests exist in `test/test.py`

### Works Cited

General HTML Templates, CSS, js credit to Colorlib https://colorlib.com/wp/template/ (Woodrox, Dup, Maxitechture) and W3Schools https://www.w3schools.com/howto/ (buttons, styles, error page)

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTMwNTQ0NjcxXX0=
-->

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTkwMDU4ODI5OSw3NjMwNDc2NTcsMTQyMz
g4NTAxNCwxODc4NjkxMzE5LC0xNDAwNzk2NjkwLC0xNTAzMTU5
OTc4LC0xNzE0MzQxNTgyLDg3MDMzODU3NV19
-->