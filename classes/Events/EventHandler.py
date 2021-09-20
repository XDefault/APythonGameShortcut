from classes.InputSystem.InputClass import Input
from classes.Events.EventClass import Event

class __EventHandler:

    eventsLoopCheck = []
    eventsSingleCheck = []
    

    def AddEventToLoopCheck(self,event):                        #Add a event to be execute multiple times
        if(self.eventsLoopCheck.__contains__(event) == False):
            self.eventsLoopCheck.append(event)

    def AddEventToSigleCheck(self,event):                       #Add a event to be execute one single time
        if(self.eventsSingleCheck.__contains__(event) == False):
            self.eventsSingleCheck.append(event)

    def EventsLoopCheck(self):                                  #Execute events in the loop list
        for e in self.eventsLoopCheck:
            e.Execute()

    def EventsSingleCheck(self):                                #Execute events in the single list and remove the event from it
        for e in self.eventsSingleCheck:
            e.Execute()
            self.eventsSingleCheck.remove(e)

__staticEventHandler = __EventHandler()

def GetStaticHandler():
    global __staticEventHandler
    if(__staticEventHandler == None):
        try:
            __staticEventHandler = __EventHandler()
        except:
            raise TypeError
    return __staticEventHandler