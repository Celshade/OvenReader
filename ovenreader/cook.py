from textwrap import dedent as dd


class Cook(object):
    """Maintain parsed cook data.

    This object maintains unique cook data and is intended to be used in
    conjunction with OvenReader(). Main attributes are specified in a
    [required] pre-configured dict argument.

    Args:
        data: Configuration of attributes.

    Attributes:
        NAME (str): File name OF the cook.
        PRODUCT (str): Product ID.
        LOT (str): Product lot number.
        OVEN (str): Oven ID.
        PROGRAM (str): Program name.
        START_TIME (str): Cook start time.
        START_TEMPS (tuple[float]): Starting temperatures.
        END_TIME (str): Cook end time.
        END_TEMPS (tuple[float]): Ending temperatures.
        STAGES (dict): Stage information.
        COMMENTS (list): Cook comments.
        ERRORS (list): Cook errors.
        IN_WEIGHT (int): Product in-weight.
        OUT_WEIGHT (int): Product out-weight.
        OVEN_YIELD (float): Product yield.
        DURATION (str): Total duration of cook.
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
        self.STAGES = data["stages"]
        self.COMMENTS = data["comments"]
        self.ERRORS = data["errors"]
        self.IN_WEIGHT = data["in_weight"]
        self.OUT_WEIGHT = data["out_weight"]
        self.COOK_YIELD = self.OUT_WEIGHT / self.IN_WEIGHT
        self.DURATION = int(sum(self.STAGES.values()))

    def _to_hours(self, raw_minutes: int) -> str:
        """Return a string representation of hours and minutes.

        Args:
            raw_minutes: The number of minutes to represent.
        """
        hours, minutes = int(raw_minutes // 60), int(raw_minutes % 60)
        return f"{hours} hr {minutes} min"

    def _wrapper(self, header: str, border: str) -> str:
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

    def compile_data(self, comments: bool, errors: bool) -> str:
        """Return a formatted string of data points.

        Args:
            comments: Flag to control the output of comments (default=False).
            errors: Flat to control the output of errors (default=False).
        """
        output = '\n'.join((
            (f"\nFile: {self.NAME}"),  # TODO Remove??
            (self._wrapper("[Cook Info]", '=')),
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
            In-weight: {self.IN_WEIGHT}
            Out-weight: {self.OUT_WEIGHT}
            Yield: NotYetImplemented
            """)),
            (self._wrapper("[Stage Info]", '=')),
        ))
        # Compile stage data.
        for stage, duration in self.STAGES.items():
            output += f"\n{stage}: {int(duration)} minutes"
        # TODO Implement comments and error output
        return output
