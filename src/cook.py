"""Establish the Cook object.

Intended to be imported and used by the OvenReader class.

Classes:
    Cook(object): An object that stores cook data.
"""
from typing import Union
from textwrap import dedent as dd


class Cook(object):
    """Maintain parsed cook data.

    This object maintains unique cook data and is intended to be used in
    conjunction with an OvenReader object. Main attributes are specified in a
    pre-configured dict.

    Args:
        data: Configuration of attributes.

    Attributes:
        NAME (str): File name of the cook.
        PRODUCT (str): Product ID.
        LOT (str): Product lot number.
        OVEN (str): Oven ID.
        PROGRAM (str): Program name.
        START_TIME (datetime): Cook start time.
        START_TEMPS (list[float]): Starting temperatures.
        END_TIME (datetime): Cook end time.
        END_TEMPS (list[float]): Ending temperatures.
        DURATION (int): Total duration of the cook (in minutes).
        STAGES (dict): Stage information.
        COMMENTS (list[str]): Cook comments.
        ERRORS (list[str]): Cook errors.
        IN_WEIGHT (int): Product in-weight.
        OUT_WEIGHT (int): Product out-weight.
        OVEN_YIELD (float): Product yield.
    Public Methods:
        compile_data(): Compile formatted data points.
    """

    def __init__(self, data: dict) -> None:
        self.NAME = data["fname"]
        self.PRODUCT = data["product"]
        self.LOT = data["lot"]
        self.OVEN = data["oven"]
        self.PROGRAM = data["program"]
        self.START_TIME = data["start_time"]
        self.START_TEMPS = data["start_temps"]
        self.END_TIME = data["end_time"]
        self.END_TEMPS = data["end_temps"]
        self.DURATION = data["duration"]
        self.STAGES = data["stages"]
        self.COMMENTS = data["comments"]
        self.ERRORS = data["errors"]
        self.IN_WEIGHT = data["in_weight"]
        self.OUT_WEIGHT = data["out_weight"]
        self.COOK_YIELD = data["cook_yield"]

    def _wrapper(self, header: str, border: str='=') -> str:
        """Return a centered header, wrapped with a border.

        Args:
            header: The header to wrap.
            border: The border symbol to wrap the header with.
        """
        wrap = border * 79
        return dd(f"""
        {wrap}
        {header.center(79)}
        {wrap}""")

    def _to_hours(self, raw_minutes: int) -> str:
        """Return a string representation of hours and minutes.

        Args:
            raw_minutes: The number of minutes to represent.
        """
        hours, minutes = int(raw_minutes // 60), int(raw_minutes % 60)
        return f"{hours} hr {minutes} min"

    def _check_val(self, value: int) -> Union[int, str]:
        """Return a message if no value was configured, else return value.

        This function is used to generate the appropriate weight/yield output
        for the compile_data function, where a value of -1 == no value having
        been specified.

        Args:
            value: The configuration value.
        """
        return value if value != -1 else "NA"

    def compile_data(self, comments: bool, errors: bool) -> str:
        """Return a formatted string of data points.

        Args:
            comments: Flag to control the output of comments.
            errors: Flag to control the output of errors.
        """
        # Compile cook data and stage info header.
        output = '\n'.join((
            ('\n' + f"File: {self.NAME}".center(79)),
            (self._wrapper("[Cook Info]")),
            (dd(f"""
            Product: {self.PRODUCT}
            Lot: {self.LOT}
            Oven: {self.OVEN}
            Program {self.PROGRAM}
            Start: {self.START_TIME}
            Starting Temps: {self.START_TEMPS}
            End: {self.END_TIME}
            Ending Temps: {self.END_TEMPS}
            Duration: {self.DURATION} minutes [{self._to_hours(self.DURATION)}]
            In-weight: {self._check_val(self.IN_WEIGHT)}
            Out-weight: {self._check_val(self.OUT_WEIGHT)}
            Yield: {self._check_val(self.COOK_YIELD)} \
            """)),
            (self._wrapper("[Stage Info]", '=')),
            ('')  # Add a blank space between 'Stage Info' header and data
        ))
        # Compile stage data.
        for stage, duration in self.STAGES.items():
            output += f"\n{stage}: {int(duration)} minutes"
        # TODO Implement comments and error output
        return output + '\n'
