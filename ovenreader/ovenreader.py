"""Establish a parser to read oven data from a .txt file."""
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

    def parse(self, path: str) -> Cook:
        """Parse the file and return a Cook object.

        Args:
            path: The file path
        """

        # TODO Finish implementation
        # Attribute configuration for Cook()
        config = {
            "product": None,
            "lot": None,
            "in_weight": None,
            "out_weight": None,
            "end_time": None
        }
        # Obtain file name
        config["fname"] = path[path.rfind('\\') + 1:].strip()

        with open(path, 'r') as f:
            text = f.readlines()
            # Isolate the header, containing program & start time
            header = text[1].split(',')
            config["program"] = header[1]
            start_info = header[3].replace('/', '-').strip()
            config["start_time"] = dt.strptime(start_info, "%m-%d-%Y %H:%M:%S")
            # Obtain oven number
            config["oven"] = text[2].split(',')[1][5:].strip()

            # Iterate through file data and calculate stage durations
            counter = dt.strptime("00:00", "%H:%M")
            curr_stage = 1
            stages = {}  # Stages to be added to config, once complete
            for line in text:
                if line.strip().endswith(",,"):  # Targets cook data
                    this_line = line.split(',')

                    if this_line[2] == "START":
                        # TODO Parse starting temperatures
                        continue
                    elif this_line[2] == "END":
                        # TODO Parse end time
                        # TODO Parse final temperatures
                        continue
                    elif int(this_line[2]) > curr_stage:
                        # Update (*maintain sequence)
                        clock = dt.strptime(this_line[0], "%H:%M")
                        time = (clock - counter).total_seconds() / 60
                        stages[f"Stage {curr_stage}"] = time
                        counter = clock
                        curr_stage += 1
                # TODO parse product and lot info
            config["stages"] = stages
        return Cook(config)

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
        wrap = border * 80
        return dd(f"""
        {wrap}
        {header.center(80)}
        {wrap}""")

    def output(self, cook: Cook,
               comments: bool=False, errors: bool=False) -> None:
        """Return a formatted output of data points.

        Args:
            comments: Flag to control the output of comments (default=False).
            errors: Flat to control the output of errors (default=False).
        """
        # TODO Fix yield
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
        End: {cook.END_TIME}
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
