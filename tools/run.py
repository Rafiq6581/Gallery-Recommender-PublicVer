from datetime import datetime as dt
from pathlib import Path

from loguru import logger
import click 

from pipelines.digital_data_etl import digital_data_etl
from pipelines.feature_engineering import feature_engineering
from pipelines.end_to_end import end_to_end


@click.command(
    help=""".
This is the main entry point for the pipelines. 
This is where everything comes together. 

You can run the pipeline with the following command:

Example:
```
poetry run python run.py --run-etl
```
"""
)


@click.option(
    "--no-cache",
    is_flag=True,
    default=False,
    help="Do not use cached data",
)

@click.option(
    "--run-end-to-end-data",
    is_flag=True,
    default=False,
    help="Whether to run all the data pipelines in one go.",
)

@click.option(
    "--run-etl",
    is_flag=True,
    default=False,
    help="Run the ETL pipeline",
)


@click.option(
    "--run-feature-engineering",
    is_flag=True,
    default=False,
    help="Run the feature engineering pipeline",
)

@click.option(
    "--etl-config-filename",
    default="digital_data_etl_artomo.yaml",
    help="The path to the ETL config file",
)

@click.option(
    "--reflections",
    is_flag=True,
    default=False,
    help="Run the ETL pipeline with reflections",
)


def main(
    no_cache: bool = False,
    run_end_to_end_data: bool = False,
    run_etl: bool = False,
    etl_config_filename: str = "digital_data_etl_artomo.yaml",
    etl_reflections_config_filename: str = "digital_data_etl_reflections.yaml",
    run_feature_engineering: bool = False,
    reflections: bool = False,
) -> None:
    assert (
        run_etl 
        or run_feature_engineering
        or run_end_to_end_data
    ), "You must specify at least one of the following options: --run-etl or --run-feature-engineering"


    pipeline_args = {
        "enable_cache": not no_cache,
    }
    
    root_dir = Path(__file__).resolve().parent.parent


    if run_etl:
        run_args_etl = {}
        pipeline_args["config_path"] = root_dir / "configs" / etl_config_filename
        assert pipeline_args["config_path"].exists(), f"Config file not found: {pipeline_args['config_path']}"
        pipeline_args["run_name"] = f"digital_data_etl_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        digital_data_etl.with_options(**pipeline_args)(**run_args_etl)

    if run_end_to_end_data:
        run_args_end_to_end_data = {}
        pipeline_args["config_path"] = root_dir / "configs" / etl_config_filename
        assert pipeline_args["config_path"].exists(), f"Config file not found: {pipeline_args['config_path']}"
        pipeline_args["run_name"] = f"end_to_end_data_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        end_to_end.with_options(**pipeline_args)(**run_args_end_to_end_data)

    if reflections:
        run_args_reflections = {}
        pipeline_args["config_path"] = root_dir / "configs" / "digital_data_etl_reflections.yaml"
        pipeline_args["run_name"] = f"reflections_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        digital_data_etl.with_options(**pipeline_args)(**run_args_reflections)

    if run_feature_engineering:
        run_args_feature_engineering = {}
        pipeline_args["run_name"] = f"feature_engineering_run_{dt.now().strftime('%Y_%m_%d_%H_%M_%S')}"
        feature_engineering.with_options(**pipeline_args)(**run_args_feature_engineering)



if __name__ == "__main__":
    main()
