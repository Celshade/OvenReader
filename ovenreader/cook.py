# TODO implement
class Cook(object):
    """Maintain parsed cook data.

    Intended to be initialized with a dictionary of attributes, which
    are then unpacked. This object is intended to be a container for
    unique 'cook' data

    Attributes:
        data: A dictionary of attributes and their values.
    """

    def __init__(self, data: dict=None) -> None:
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
        # TODO implement comments and errors
        # self._comments = []  # list of tules containing comment data
        # self._errors = []  # list of tuples containing error data

        # TODO unpack data (dict) into attributes
        # raise NotImplementedError("Class not implemented.")

        print(self.__dict__.items())


if __name__ == "__main__":
    # TODO remove tests
    test = Cook()
