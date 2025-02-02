import logging
import pathlib
from typing import Union, Type

import mwcp
from mwcp.runner import Runner
from mwcp.report import Report
from mwcp.parser import Parser
from mwcp import metadata


def run(
        parser: Union[str, Type[Parser]],
        file_path: Union[str, pathlib.Path] = None,
        data: bytes = None,
        *,
        output_directory: Union[str, pathlib.Path] = None,
        include_file_data: bool = False,
        prefix_output_files: bool = True,
        include_logs: bool = True,
        log_level: int = None,
        log_filter: logging.Filter = None,
) -> Report:
    """
    Runs a specified parser on a given file path or data.

    :param parser: Name or class of parser to run
        (use ":" notation to specify source if necessary e.g. "acme:Foo")
    :param file_path: File path to parse
    :param data: File data to parse
    :param output_directory:
        sets directory for output_file(). Should not be written to (or read from) by parsers
        directly (use tempdir)
        If not provided, files will not be written out.
    :param include_file_data: Whether to include file data in the generated report.
        If disabled, only metadata such as the file path, description, and md5 will be included.
    :param prefix_output_files: Whether to includes a prefix of the first 5 characters
        of the md5 on output files. This is to help avoid overwriting multiple
        output files with the same name.
    :param include_logs: Whether to include error and debug logs in the generated report.
    :param log_level: If including logs, the logging level to be collected.
        (Defaults to currently set effective log level)
    :param log_filter: If including logs, this can be used to pass in a custom filter for the logs.
        Should be a valid argument for logging.Handler.addFilter()

    :return: mwcp.Report object containing parse results.
    """
    if file_path:
        file_path = str(file_path)
    runner = Runner(
        output_directory=output_directory,
        include_file_data=include_file_data,
        prefix_output_files=prefix_output_files,
        include_logs=include_logs,
        log_level=log_level,
        log_filter=log_filter,
    )
    return runner.run(parser, file_path=file_path, data=data)


def schema(id=None) -> dict:
    """
    Generates a JSON Schema for a Report object.
    NOTE: This is the schema for a single report. Depending on how you use MWCP,
    you may get a list of these reports instead.
    """
    if id is None:
        id = (
            f"https://raw.githubusercontent.com/Defense-Cyber-Crime-Center/DC3-MWCP/"
            f"{mwcp.__version__}/mwcp/config/schema.json"
        )
    schema = {
        "$schema": "https://json-schema.org/draft/2019-09/schema",
        "$id": id,
    }
    schema.update(metadata.Report.schema())

    # "output_text" may also be included if we are running from the server service.
    schema["properties"]["output_text"] = {
        "type": "string",
        "description": "Raw text output from MWCP.",
    }

    return schema
