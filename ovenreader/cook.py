# TODO implement
class Cook(object):
    """Maintain parsed cook data.

    This object is intended to be used in conjunction with OvenReader() and
    maintains unique cook data. Attributes are specified in a pre-configured
    dict.

    Args:
        data: Configruation of attributes.

    Attributes:
        file_name (str): File name for the cook.
        product (str): Product ID.
        lot (str): Product lot number.
        in_weight (int): Product in-weight.
        out_weight (int): Product out-weight.
        oven_yield (float): Product yield.
        oven (str): Oven ID.
        program (str): Program name.
        start_time (str): Cook start time.
        end_time (str): Cook end time.
        duration (str): Total duration of cook.
        stages (dict): Stage information.
        comments (list): Cook comments.
        errors (list): Cook errors.
    """

    def __init__(self, data: dict) -> None:
        self.file_name = data["fname"]
        self.product = data["product"]
        self.lot = data["lot"]
        self.in_weight = data["in_weight"]
        self.out_weight = data["out_weight"]
        self.cook_yield = data["yield"]
        self.oven = data["oven"]
        self.program = data["program"]
        self.start_time = data["start_time"]
        self.end_time = data["end_time"]
        self.duration = data["duration"]
        self.stages = data["stages"]
        self.comments = data["comments"]
        self.errors = data["errors"]


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
    except KeyError:
        print("\nConfiguration failed...")
        print("Deleting object...")
    print(help(Cook))
