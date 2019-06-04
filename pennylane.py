import logging
import argparse

import yaml
import pandas as pd
import pickle

import src.generate_features as gf

logging.config.fileConfig("config/logging/local.conf")


class PennyLane:
    def __init__(self, model_config, debug=False):

        # Set up logger and put in debug mode if debug = True
        self.logger = logging.getLogger("pennylane-score")
        if debug:
            self.logger.setLevel("DEBUG")
        self.logger.debug("Logger is in debug model")

        # Load model configuration fle
        with open(model_config, 'r') as f:
            config = yaml.load(f)

        self.logger.info("Configuration file loaded from %s", model_config)
        self.config = config

        # Load in configurations for generating features
        self.make_categorical = config["generate_features"]["make_categorical"]
        self.bin_values = config["generate_features"]["bin_values"]
        self.choose_features = config["score_model"]["choose_features"]

        # Load trained model object
        path_to_tmo = config["score_model"]["path_to_tmo"]
        with open(path_to_tmo, "rb") as f:
            self.tmo = pickle.load(f)

        self.logger.info("Trained model object loaded from %s", path_to_tmo)

        # Load in prediction parameters
        self.predict = {} if "predict" not in config["score_model"] else config["score_model"]["predict"]

    def run(self, data):
        """Predicts song popularity for the input data

        Args:
            data (:py:class:`pandas.DataFrame`): DataFrame containing the data inputs for scoring

        Returns:
            results (:py:class:`numpy.Array`): Array of predictions of song popularity

        """

        # Generate features
        data = gf.make_categorical(data, **self.make_categorical)
        data = gf.bin_values(data, **self.bin_values)
        self.logger.info("Features generated")

        # Choose which features to use
        features = gf.choose_features(data, **self.choose_features)
        self.logger.info("Features being used are: %s", ",".join(features.columns.tolist()))

        # Make predictions
        results = self.tmo.predict(features, **self.predict)
        self.logger.info(dict(predictions=results))

        return results


def run_pennylane(args):
    data_df = pd.read_csv(args.input)

    pennylane_instance = PennyLane(args.config, args.debug)

    results = pennylane_instance.run(data_df)

    if args.output is not None:
        results.to_csv(args.output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict song popularity")
    parser.add_argument("--config", "-c", default="config/test_model_config.yml",
                        help="Path to the test configuration file")
    parser.add_argument("--input", "-i", default="data/sample/data_to_score.csv",
                        help="Path to input data for scoring")
    parser.add_argument("--output", "-o",  default=None,
                        help="Path to where to save output predictions")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="If given, logger will be put in debug mode")
    args = parser.parse_args()

    run_pennylane(args)