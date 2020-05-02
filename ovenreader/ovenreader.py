"""Read oven data from a .txt file and output critical data points."""
from datetime import datetime as dt

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

    def _get_weight(self, text: str) -> int:
        """Return the weight found within the given line of text.

        Args:
            text: The string to iterate over.
        """
        start = text.index(':') + 1
        return int(text[start:].strip())

    def parse(self, path: str) -> None:
        """Parse the file and establish a configured Cook object.

        Parse critical data points from raw text and encapsulate them into
        a Cook object.

        Args:
            path: The file path to the text.
        """
        config = {}  # Cook attribute configuration
        # Obtain filename, product, and lot.
        file_name = path[path.rfind('\\') + 1:].strip()
        config["fname"] = file_name
        config["product"], config["lot"] = file_name.strip(".txt").split('_')

        with open(path, 'r') as f:
            text = f.readlines()
            # Obtain program, start time, and oven number.
            header = text[1].split(',')  # Isolate the report header.
            config["program"] = header[1]
            start_info = header[3].replace('/', '-').strip()
            config["start_time"] = dt.strptime(start_info, "%m-%d-%Y %H:%M:%S")
            config["oven"] = text[2].split(',')[1][5:].strip()
            counter = dt.strptime("00:00", "%H:%M")
            curr_stage = 1
            stages = {}  # Stages will be added to config, once complete

            # Iterate over the main text body.
            for this_line in text:
                if this_line.strip().endswith(",,"):  # Target cook data
                    line = this_line.split(',')

                    # Obtain starting temperatures.
                    if line[2] == "START":
                        config["start_temps"] = self._get_temps(line)
                    # Obtain end time and temperatures.
                    elif line[2] == "END":
                        config["end_temps"] = self._get_temps(line)
                        config["end_time"] = "NotYetImplemented"
                    # Obtain stage data.
                    elif int(line[2]) > curr_stage:
                        clock = dt.strptime(line[0], "%H:%M")
                        time = (clock - counter).total_seconds() / 60
                        stages[f"Stage {curr_stage}"] = time
                        counter = clock
                        curr_stage += 1

                # Obtain in and out weights.
                elif this_line.startswith("In-weight:"):
                    config["in_weight"] = self._get_weight(this_line)
                elif this_line.startswith("Out-weight:"):
                    config["out_weight"] = self._get_weight(this_line)
                else:
                    config["in_weight"], config["out_weight"] = 1, -1
            config["stages"] = stages
            # TODO Parse Comments and Errors
            config["comments"], config["errors"] = [], []
        self._current_cook = Cook(config)

    def output(self, comments: bool=False, errors: bool=False) -> None:
        """Output formatted cook data for the current cook.

        Args:
            comments: Flag to control the output of comments (default=False).
            errors: Flag to control the output of errors (default=False).
        """
        # TODO Add flags to output comments | errors
        print(self._current_cook.compile_data(comments, errors))


if __name__ == "__main__":
    # TODO Remove tests once complete.
    print("\n***TESTING***")
    reader = OvenReader()
    reader.parse("..\\docs\\404E_PL123456L.txt")
    reader.output()
