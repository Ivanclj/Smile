"""
Created on 5/10/19

@author: ivan chen

"""

import numpy as np
import logging
import requests
import argparse
import yaml
import pandas as pd

logger = logging.getLogger(__name__)


def download_data(read_path):
    df = pd.read_csv(read_path,index_col=0)
    return df

def run_loading(args):
    """Loads config and executes load data set
    Args:
        args: passed in argparser
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    config = config['load_data']

    df = download_data(config["download_data"]['read_path'])

    if args.savecsv is not None:
        df.to_csv(args.savecsv)
    else:
        df.to_csv(config["download_data"]['save_path'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', default= '../config/config.yml',help='path to yaml file with configurations')
    parser.add_argument('--savecsv', help='Path to where the dataset should be saved to (optional)')

    args = parser.parse_args()

    run_loading(args)