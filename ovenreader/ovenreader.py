"""Establish a parser to read oven data from a .txt file."""
import os
from textwrap import dedent as dd
from datetime import datetime as dt

# TODO encapsulate data into Cook() object.
class OvenReader(object):
    """Parse and output raw cook data.

    OvenReader parses raw cook data (in the form of a .txt file) to create a
    Cook() object and output data in an easy to read format.

    Public Methods:
        parse(): Parse data.
        output(): Output formatted data.
    """

    def __init__(self) -> None:
        self._fpath = None
        self._in_weight = None
        self._out_weight = None
        self._lot = None
        self._product = None
        self._oven = None
        self._program = None
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._yield = None
        self._stages = {}  # dict containing stage data

    def parse(self, path: str,
              in_weight: int=0, out_weight: int=0) -> None:
        """Parse the outer limits of the file.

        Args:
            path: The file path
            in_weight: The product in-weight (default=-1 -> no input)
            out_weight: The product out-weight (default=-1 -> no input)
        """
        # TODO Update to handle Cook() object
        self._fpath = path
        self._in_weight = None if in_weight == 0 else in_weight
        self._out_weight = None if out_weight == 0 else out_weight

        with open(path, 'r') as f:
            # Read file content
            text = f.readlines()
            # Isolate the header, containing program & start time
            header = text[1].split(',')
            self._program = header[1]
            # Format date info and create datetime object
            st_info = header[3].replace('/', '-').strip()
            self._start_time = dt.strptime(st_info, "%m-%d-%Y %H:%M:%S")
            # Parse oven number
            self._oven = text[2].split(',')[1][5:].strip()

            # Iterate through file data and calculate stage durations
            counter = dt.strptime("00:00", "%H:%M")
            curr_stage = 1
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
                        self._stages[f"Stage {curr_stage}"] = time
                        counter = clock
                        curr_stage += 1

                # TODO parse product and lot info
        # Calculate cook duration
        self._duration = int(sum(self._stages.values()))

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

    def output(self, comments: bool=False, errors: bool=False) -> None:
        """Return a formatted output of data points.

        Args:
            comments: Flag to control the output of comments (default=False).
            errors: Flat to control the output of errors (default=False).
        """
        # TODO Update to handle Cook() object
        # TODO Add flags to output comments | errors
        # Output cook data
        print(f"\nFile: {self._fpath}", end='')  # TODO Remove??
        print(self._wrapper("[Cook Info]", '='), end='')
        print(dd(f"""
        Product: {self._product}
        Lot: {self._lot}
        Oven: {self._oven}
        In-weight: {self._in_weight}
        Out-weight: {self._out_weight}
        Yield: {self._yield}
        Program {self._program}
        Start: {self._start_time}
        End: {self._end_time}
        Duration: {self._duration} minutes [{self._to_hours(self._duration)}] \
        """), end='')

        # Output stage data
        print(self._wrapper("[Stage Info]", '='))

        for stage, duration in self._stages.items():
            print(f"{stage}: {int(duration)} minutes")


if __name__ == "__main__":
    # TODO Remove tests once complete
    test = OvenReader()
    test.parse("..\\documents\\404E_PL123456L.txt")
    test.output()
