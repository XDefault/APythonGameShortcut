class Event:
    def __init__(self,_event):
        self.event = _event

    def execute(self):
        raise NotImplementedError       #Override this method to avoid the error
