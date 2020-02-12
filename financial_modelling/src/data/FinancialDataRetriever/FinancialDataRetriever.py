import datetime as dt
import json
import logging
import pathlib


class FinancialDataRetriever:
    """
    Base class for data retrievers.
    """

    def __init__(self):
        logging.basicConfig(level=logging.ERROR)
        self.logger = logging.getLogger()


    def generate_output_filepath(self, *args, output_directory=None):
        """
        Generates the output filepath for data to be written to

        Parameters
        ----------
            *args : array
                Array of strings to use to generate the filename
            output_directory : str
                The specified directory to output the file to. If unspecified,
                the file will be written to the pwd.
        Returns
        -------
            output_filepath : str
                The filepath generated
        """
        file_date = dt.datetime.now().strftime("%Y%m%d%H%M%S")
        args_name = "_".join([str(a) for a in args])
        output_filepath = pathlib.Path(f"{args_name}_{file_date}.json")
        if output_directory is not None:
            output_filepath = pathlib.Path(output_directory).joinpath(
                output_filepath
            )
        return output_filepath

    def handle_api_request(self, request, *args, output_directory=None):
        """
        Handles requests objects to either write the output if successful

        Parameters
        ----------
            request : request.models.Response
                A request made to an API endpoint
            *args : array
                Array of strings to use to generate the filename
            output_directory : str
                The specified directory to output the file to. If unspecified,
                the file will be written to the pwd.
        Returns
        -------
            request : request.models.Response
                A request made to an API endpoint
        """
        if request.status_code == 200:
            output_filepath = self.generate_output_filepath(
                *args, output_directory=output_directory
            )
            with open(output_filepath, "w") as f:
                json.dump(request.json(), f)
        else:
            self.logger.error("Request did not return status code 200.")
        return request
