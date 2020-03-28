class Cook(object):
    """Maintain parsed cook data.

    This object is intended to be used in conjunction with OvenReader() and
    maintains unique cook data. Main attributes are specified in a
    pre-configured dict.

    Args:
        data: Configruation of attributes.

    Attributes:
        NAME (str): File name OF the cook.
        PRODUCT (str): Product ID.
        LOT (str): Product lot number.
        IN_WEIGHT (int): Product in-weight.
        OUT_WEIGHT (int): Product out-weight.
        OVEN (str): Oven ID.
        PROGRAM (str): Program name.
        START_TIME (str): Cook start time.
        START_TEMPS (tuple[float]): Starting temperatures.
        END_TIME (str): Cook end time.
        END_TEMPS (tuple[float]): Ending temperatures.
        STAGES (dict): Stage information.
        COMMENTS (list): Cook comments.
        ERRORS (list): Cook errors.
        OVEN_YIELD (float): Product yield.
        DURATION (str): Total duration of cook.
    """

    def __init__(self, data: dict) -> None:
        self.NAME = data["fname"]
        self.PRODUCT = data["product"]
        self.LOT = data["lot"]
        self.IN_WEIGHT = data["in_weight"]
        self.OUT_WEIGHT = data["out_weight"]
        self.OVEN = data["oven"]
        self.PROGRAM = data["program"]
        self.START_TIME = data["start_time"]
        self.START_TEMPS = data["start_temps"]
        self.END_TIME = data["end_time"]
        self.END_TEMPS = data["end_temps"]
        self.STAGES = data["stages"]
        # TODO self.COMMENTS = data["comments"]
        # TODO self.ERRORS = data["errors"]
        self.COOK_YIELD = self.OUT_WEIGHT / self.IN_WEIGHT
        self.DURATION = int(sum(self.STAGES.values()))


if __name__ == "__main__":
    # TODO remove tests
    TEST_CONFIG = {
        "fname": ".\\path",
        "product": "404E",
        "lot": "PL123456L",
        "in_weight": 420,
        "out_weight": 110,
        "yield": .50,
        "oven": "V5",
        "program": '3',
        "start_time": "1/1/2020 00:00",
        "end_time": "1/2/20 00:00",
        "duration": 560,
        "stages": {},
        "comments": [],
        "errors": []
    }
    try:
        test = Cook(TEST_CONFIG)
        print("\n***[TESTING]***")
        print("\nSuccessful instantiation\n")
        print("-" * 42)
    except KeyError:
        print("\nConfiguration failed...")
        print("Deleting object...")
    print(help(Cook))
