
def setup(pin, mode):
    pass


def output(pin, mode):
    pass


def setmode(board):
    pass


def cleanup():
    pass


class PWM(object):
    pin = 0
    val = 0

    def __init__(self, pin, val, **kwargs):
        super(PWM, self).__init__(**kwargs)

    def start(self, *args):
        pass

    def stop(self, *args):
        pass

    def ChangeDutyCycle(self, *args):
        pass


__name__ = 'Dummy.GPIO'

OUT = None
BOARD = None
HIGH = None
LOW = None

