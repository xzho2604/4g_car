from pyPS4Controller.controller import Controller

class MyController(Controller):
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    # overriding methods of the events


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()

