#!/usr/bin/env python
"""
-
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    artifact_phat = run.use_artifact(args.input_artifact).file()
    
    df = pd.read_csv(artifact_phat)
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.info(f"Removing outliers with price outside range: {args.min_price} - {args.max_price}")
    df = df[df['price'].between(args.min_price, args.max_price)].copy()

    cleaned_file_path = "clean_sample.csv"
    df.to_csv(cleaned_file_path, index=False)
    logger.info(f"Cleaned data saved to {cleaned_file_path}")

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(cleaned_file_path)
    run.log_artifact(artifact)

    logger.info("Cleaned data uploaded successfully.")
    run.finish()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Path to the input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Type of the output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to consider for filtering the dataset",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price to consider for filtering the dataset",
        required=True
    )


    args = parser.parse_args()

    go(args)
