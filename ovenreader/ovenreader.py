"""Read oven data from a .txt file and output critical data points."""
import os
from datetime import datetime as dt
from textwrap import dedent as dd

from cook import Cook


class OvenReader(object):
    """Parse and output raw cook data.

    OvenReader parses raw cook data (in the form of a .txt file) to create a
    Cook() object and output data in an easy to read format.

    Public Methods:
        parse(): Parse data.
        output(): Output formatted data.
    """

    def __init__(self) -> None:
        self._current_cook = None

    def _get_temps(self, text: str) -> list:
        """Return a list of strings containing relevant temperatures.

        Iterate over a string and ignore invalid characters.

        Args:
            text: The text to parse.
        """

        chars = ('D', '', '\n')
        temps = [i for i in text[8:] if i not in chars]

        return temps

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

    def parse(self, path: str) -> Cook:
        """Parse the file and return a Cook object.

        Parse critical data points from the raw data and consolidate them into
        a Cook object.

        Args:
            path: The path to the data.
        """

        config = {}  # Cook attribute configuration
        # Obtain file name, product ID, and lot number
        file_name = path[path.rfind('\\') + 1:].strip()
        config["fname"] = file_name
        config["product"], config["lot"] = file_name.split('_')

        # Parse the file
        with open(path, 'r') as f:
            text = f.readlines()
            # Obtain program, start time, and oven number
            header = text[1].split(',')  # Isolate the report header
            config["program"] = header[1]
            start_info = header[3].replace('/', '-').strip()
            config["start_time"] = dt.strptime(start_info, "%m-%d-%Y %H:%M:%S")
            config["oven"] = text[2].split(',')[1][5:].strip()

            # Iterate through file data
            counter = dt.strptime("00:00", "%H:%M")  # Time counter
            curr_stage = 1  # Stage counter
            stages = {}  # Stages to be added to config, once complete
            for this_line in text:
                if this_line.strip().endswith(",,"):  # Target cook data
                    line = this_line.split(',')

                    # Obtain starting temperatures
                    if line[2] == "START":
                        config["start_temps"] = self._get_temps(line)
                    # Obtain end time and temperatures
                    elif line[2] == "END":
                        config["end_temps"] = self._get_temps(line)
                        config["end_time"] = "NotYetImplemented"
                    elif int(line[2]) > curr_stage:
                        clock = dt.strptime(line[0], "%H:%M")
                        time = (clock - counter).total_seconds() / 60
                        stages[f"Stage {curr_stage}"] = time
                        counter = clock
                        curr_stage += 1

                # Obtain in and out weights
                # TODO consolidate weight lookups into a function
                elif this_line.startswith("In-weight:"):
                    config["in_weight"] = int(line[line.index(': ') + 1:])
                elif this_line.startswith("Out-weight:"):
                    config["out_weight"] = int(line[line.index(': ') + 1:])
                else:
                    config["in_weight"], config["out_weight"] = 1, -1
            # Obtain stage data
            config["stages"] = stages
        return Cook(config)

    def output(self, cook: Cook,
               comments: bool=False, errors: bool=False) -> None:
        """Return a formatted output of data points.

        Args:
            comments: Flag to control the output of comments (default=False).
            errors: Flat to control the output of errors (default=False).
        """
        # TODO Add flags to output comments | errors
        # Output cook data
        print(f"\nFile: {cook.NAME}", end='')  # TODO Remove??
        print(self._wrapper("[Cook Info]", '='), end='')
        print(dd(f"""
        Product: {cook.PRODUCT}
        Lot: {cook.LOT}
        Oven: {cook.OVEN}
        In-weight: {cook.IN_WEIGHT}
        Out-weight: {cook.OUT_WEIGHT}
        Yield: NotYetImplemented
        Program {cook.PROGRAM}
        Start: {cook.START_TIME}
        Starting Temps: {cook.START_TEMPS}
        End: {cook.END_TIME}
        Ending Temps: {cook.END_TEMPS}
        Duration: {cook.DURATION} minutes [{self._to_hours(cook.DURATION)}] \
        """), end='')

        # Output stage data
        print(self._wrapper("[Stage Info]", '='))

        for stage, duration in cook.STAGES.items():
            print(f"{stage}: {int(duration)} minutes")


if __name__ == "__main__":
    # TODO Remove tests once complete
    test = OvenReader()
    print("\n***TESTING***")
    TEST_COOK = test.parse("..\\docs\\404E_PL123456L.txt")
    print("\nIt works")
    test.output(TEST_COOK)
