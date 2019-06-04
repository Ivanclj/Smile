"""Enables the command line execution of multiple modules within src/

This module combines the argparsing of each module within src/ and enables the execution of the corresponding scripts
so that all module imports can be absolute with respect to the main project directory.

To understand different arguments, run `python run.py --help`
"""
import argparse
import logging.config
from app.app import app

# Define LOGGING_CONFIG in config.py - path to config file for setting up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger("run-penny-lane")
logger.debug('Test log')

from src.database import create_db, add_user
from src.load_data import run_loading
# from src.generate_features import run_features
# from src.train_model import run_training
# from src.score_model import run_scoring


def run_app(args):
    print(app.config)
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Run components of the model source code")
    subparsers = parser.add_subparsers()

    # Sub-parser for creating a database
    sb_create = subparsers.add_parser("create", description="Create database")
    sb_create.add_argument("--artist", default="Britney Spears", help="Artist of song to be added")
    sb_create.add_argument("--title", default="Radar", help="Title of song to be added")
    sb_create.add_argument("--album", default="Circus", help="Album of song being added.")
    sb_create.add_argument("--engine_string", default='sqlite:///data/tracks.db',
                           help="SQLAlchemy connection URI for database")
    sb_create.set_defaults(func=create_db)

    # Sub-parser for ingesting new data
    sb_ingest = subparsers.add_parser("ingest", description="Add data to database")
    sb_ingest.add_argument("--artist", default="Emancipator", help="Artist of song to be added")
    sb_ingest.add_argument("--title", default="Minor Cause", help="Title of song to be added")
    sb_ingest.add_argument("--album", default="Dusk to Dawn", help="Album of song being added")
    sb_ingest.add_argument("--engine_string", default='sqlite:///data/tracks.db',
                           help="SQLAlchemy connection URI for database")
    sb_ingest.set_defaults(func=add_user)

    sb_load = subparsers.add_parser("load_data", description="Load data into a dataframe")
    sb_load.add_argument('--config', help='path to yaml file with configurations')
    sb_load.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    sb_load.set_defaults(func=run_loading)

    # # FEATURE subparser
    # sb_features = subparsers.add_parser("generate_features", description="Generate features")
    # sb_features.add_argument('--config', help='path to yaml file with configurations')
    # sb_features.add_argument('--input', default=None, help="Path to CSV for input to model scoreing")
    # sb_features.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_features.set_defaults(func=run_features)
    #
    # # TRAIN subparser
    # sb_train = subparsers.add_parser("train_model", description="Train model")
    # sb_train.add_argument('--config', help='path to yaml file with configurations')
    # sb_train.add_argument('--input', default=None, help="Path to CSV for input to model training")
    # sb_train.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_train.set_defaults(func=run_training)
    #
    # # SCORE subparser
    # sb_score = subparsers.add_parser("score_model", description="Score model")
    # sb_score.add_argument('--config', help='path to yaml file with configurations')
    # sb_score.add_argument('--input', default=None, help="Path to CSV for input to model scoring")
    # sb_score.add_argument('--output', default=None, help='Path to where the dataset should be saved to (optional')
    # sb_score.set_defaults(func=run_scoring)

    sb_run = subparsers.add_parser("app", description="Run Flask app")
    sb_run.set_defaults(func=run_app)

    args = parser.parse_args()
    args.func(args)
