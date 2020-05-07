"""Read oven data from a .txt file and output critical data points."""
from datetime import datetime as dt
from datetime import timedelta as delta

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
        """Return a list of temperatures as floats.

        Iterate over a string and ignore invalid characters.

        Args:
            text: The text to parse.
        """
        chars = ('D', '', '\n')
        temps = [float(i) for i in text[8:] if i not in chars]
        return temps

    def _get_weight(self, text: str) -> int:
        """Return the weight found within the given line of text.

        Args:
            text: The string to iterate over.
        """
        start = text.index(':') + 1
        return int(text[start:].strip())

    def _get_stage(self, line: str, counter: dt, stage: int) -> tuple:
        """Get current stage duration and update parsing counters.

        This function is used when parsing the main text body to update stage
        data.

        Args:
            line: The current line of text being parsed.
            counter: The current stage counter in use.
            stage: The current stage number.
        Returns:
            Return a tuple (stage_duration, new_counter, new_stage).
        """
        new_counter = dt.strptime(line[0], "%H:%M")
        duration = (new_counter - counter).total_seconds() / 60
        new_stage = stage + 1
        return (duration, new_counter, new_stage)

    def _get_end_time(self, start_time: dt, duration: int) -> dt:
        """Return the ending date and time of the cook.

        Args:
            start_time: The starting date and time.
            duration: The total duration of the cook (in minutes).
        """
        end_time = start_time + delta(minutes=duration)
        return end_time

    def parse(self, path: str) -> None:
        """Parse the file and instantiate a configured Cook object.

        Parse critical data points from raw text and encapsulate them into
        a Cook object.

        Args:
            path: The file path to the cook data.
        """
        config = {}  # Cook attribute configuration
        # Obtain filename, product, and lot.
        file_name = path[path.rfind('\\') + 1:].strip()
        config["fname"] = file_name
        config["product"], config["lot"] = file_name.strip(".txt").split('_')

        with open(path, 'r') as f:
            text = f.readlines()
            # Obtain program, start time, and oven number.
            header = text[1].split(',')  # Isolate the report header
            config["program"] = header[1]
            start_info = header[3].replace('/', '-').strip()
            config["start_time"] = dt.strptime(start_info, "%m-%d-%Y %H:%M:%S")
            config["oven"] = text[2].split(',')[1][5:].strip()
            counter = dt.strptime("00:00", "%H:%M")
            curr_stage = 1
            stages = {}  # Add to config once all stage data is gathered

            # Iterate over the main text body.
            for this_line in text:
                if this_line.strip().endswith(",,"):  # Target cook data
                    line = this_line.split(',')

                    # Obtain starting temperatures.
                    if line[2] == "START":
                        config["start_temps"] = self._get_temps(line)
                    # Obtain final stage duration and ending temperatures.
                    elif line[2] == "END":
                        end_dur = self._get_stage(line, counter, curr_stage)[0]
                        stages[f"Stage {curr_stage}"] = end_dur
                        config["end_temps"] = self._get_temps(line)
                    # Obtain stage data.
                    elif int(line[2]) > curr_stage:
                        _ = self._get_stage(line, counter, curr_stage)
                        stages[f"Stage {curr_stage}"], counter, curr_stage = _

                # Obtain in and out weights.
                elif this_line.startswith("In-weight:"):
                    config["in_weight"] = self._get_weight(this_line)
                elif this_line.startswith("Out-weight:"):
                    config["out_weight"] = self._get_weight(this_line)
                else:
                    config["in_weight"], config["out_weight"] = 1, -1
            config["stages"] = stages
            # TODO Parse Comments and Errors.
            config["comments"], config["errors"] = [], []

        # Calculate Cook duration and ending date/time.
        duration = int(sum(config["stages"].values()))
        config["end_time"] = self._get_end_time(config["start_time"], duration)
        config["duration"] = duration
        self._current_cook = Cook(config)  # Create the Cook object

    def output(self, comments: bool = False, errors: bool = False) -> None:
        """Output formatted cook data for the current cook.

        Args:
            comments: Flag to control the output of comments (default=False).
            errors: Flag to control the output of errors (default=False).
        """
        print(self._current_cook.compile_data(comments, errors))


if __name__ == "__main__":
    reader = OvenReader()
    reader.parse("..\\docs\\404E_PL123456L.txt")
    reader.output()
