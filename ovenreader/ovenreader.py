from textwrap import dedent as dd

"""Establish a parser to read oven data from a .txt file."""


class Parser(object):
    """Recieve and parse a text file.

    Establish an object that maintains and outputs cook data.

    Attributes:
        path: The file path.
        in_weight: The in-weight of the cook.
        out_weight: The out-weight of the cook.

    Public Methods:
        parse: Parse the data.
        output: Output formatted data.
    """

    def __init__(self, path: str, in_weight: int, out_weight: int) -> None:
        self._file = path
        self._in_weight = in_weight
        self._out_weight = out_weight
        self._lot = None
        self._product = None
        self._oven = None
        self._start_time = None
        self._end_time = None
        self._duration = None
        self._yield = None
        self._stages = {}
        self._comments = {}

    def parse(self, file: str) -> None:
        """Parse a file and set attributes.
        """
        # TODO
        raise NotImplementedError
        # try:
        #     with open(file) as f:
        #         text = f.readlines()

        #         for line in text:
        #             if line.startswith("Stage "):
        #                 self._stages[line[7]] = line

    def output(self) -> str:
        """Return a formatted output of important data points.
        """
        # TODO
        print(dd(f"""
        File: X://users//fuBar//{self._file}
        In-weight: {self._in_weight}
        Out-weight: {self._out_weight}
        """))


if __name__ == "__main__":
    test = Parser("A9", 420, 330)
    test.output()
