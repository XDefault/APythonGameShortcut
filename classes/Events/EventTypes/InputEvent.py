from classes.Events.EventClass import Event

class InputEvent(Event):
    
    def __init__(self,eventInput):
        super(InputEvent,self).__init__(eventInput)
    
    def Execute(self):
        pass