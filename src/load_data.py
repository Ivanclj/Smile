import logging
import os
import re
import argparse
import multiprocessing
import glob
import boto3
import yaml
import pandas as pd

import src.helpers.helpers as h

logger = logging.getLogger(__name__)


def get_s3_file_names(s3_prefix_path):
    """Get all file names in an s3 bucket under a prefix
    Args:
        s3_prefix_path (str): S3 path to prefix containing all files to list
    Returns: List of all S3 file locations
    """

    # parse s3 path for bucket name and prefix
    regex = r"s3://([\w._-]+)/([\w./_-]+)"
    m = re.match(regex, s3_prefix_path)
    s3bucket_name = m.group(1)
    s3prefix = m.group(2)

    # Get s3 bucket handle
    s3 = boto3.resource('s3')
    s3bucket = s3.Bucket(s3bucket_name)

    # Get all file names in the `s3bucket` with the prefix `s3prefix`
    files = []
    for object in s3bucket.objects.filter(Prefix=s3prefix):
        path_to_file = os.path.join("s3://%s" % s3bucket_name, object.key)
        files.append(path_to_file)

    return files


def get_file_names(top_dir):
    """Get all file names in a directory subtree
    Args:
        top_dir (str): The base directory from which to get list_of_files from
    Returns: List of file locations
    """

    if top_dir.startswith("s3://"):
        list_of_files = get_s3_file_names(top_dir)
    else:
        top_dir = top_dir[:-1] if top_dir[-1] == "/" else top_dir
        list_of_files = glob.glob(top_dir + '/*.csv', recursive=True)

    return list_of_files


def load_csv(path, **kwargs):
    """Wrapper function for `pandas.read_csv()` method to enable multiprocessing.
    """
    return pd.read_csv(path, **kwargs)


def load_column_as_list(path, column=0, **kwargs):
    for k in kwargs:
        logger.debug(kwargs[k])

    df = pd.read_csv(path, **kwargs)

    return df[column].tolist()


def load_csvs(file_names=None, directory=None, n_cores=1):
    """Loads multiple CSVs into a single Pandas dataframe.
    Given either a directory name (which can be local or an s3 bucket prefix) or a list of CSV files, this function
    will load all CSVs into a single Pandas DataFrame. It assumes the same schema exists across all CSVs.

    Args:
        file_names (list of str, default=None): List of files to load. If None, `directory` should be given.
        directory (str, default=None): Directory containing files to be loaded. If None, `filenames` should be given.
        n_cores (int, default=1): Number of processes (i.e. CPUs) to load csvs on.
            If -1 given, number of available CPUs will be used.
    Returns: Single dataframe with data from all files loaded
    """

    # Get list of files
    if file_names is None and directory is None:
        raise ValueError("filenames or directory must be given")
    elif file_names is None:
        file_names = get_file_names(directory)

    if n_cores == -1:
        n_cores = multiprocessing.cpu_count()

    logger.info("Utilizing {} cores".format(str(n_cores)))

    with h.Timer("Reading CSVs", logger):
        pool = multiprocessing.Pool(processes=n_cores)

        df_list = pool.map(load_csv, file_names)

        # Concatenate list of dataframes into one dataframe
        df = pd.concat(df_list, ignore_index=True)

    return df


def load_data(config):
    how = config["how"].lower()

    if how == "load_csv":
        if "load_csv" not in config:
            raise ValueError("'how' given as 'load_csv' but 'load_csv' not in configuration")
        else:
            df = load_csv(**config["load_csv"])
    elif how == "load_csvs":
        if config["load_csvs"] is None:
            raise ValueError("'how' given as 'load_csvs' but 'load_csvs' not in configuration")
        else:
            df = load_csvs(**config["load_csvs"])
    else:
        raise ValueError("Options for 'how' are 'load_csv' and 'load_csvs' but %s was given" % how)

    return df


def run_loading(args):
    """Loads config and executes load data set
    Args:
        args: From argparse, should contain args.config and optionally, args.save
            args.config (str): Path to yaml file with load_data as a top level key containing relevant configurations
            args.save (str): Optional. If given, resulting dataframe will be saved to this location.
    Returns: None
    """
    with open(args.config, "r") as f:
        config = yaml.load(f)

    df = load_data(**config["load_data"])

    if args.save is not None:
        df.to_csv(args.save)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--config', help='path to yaml file with configurations')

    parser.add_argument('--save', default=None, help='Path to where the dataset should be saved to (optional')

    args = parser.parse_args()

    run_loading(args)