class __EventHandler:

    eventsLoopCheck = []
    eventsSingleCheck = []


    def add_event_to_loop_check(self,event):                        #Add a event to be execute multiple times
        if not self.eventsLoopCheck.__contains__(event):
            self.eventsLoopCheck.append(event)

    def add_event_to_sigle_check(self,event):                       #Add a event to be execute one single time
        if not self.eventsSingleCheck.__contains__(event):
            self.eventsSingleCheck.append(event)

    def events_loop_check(self):                                  #Execute events in the loop list
        for e in self.eventsLoopCheck:
            e.execute()

    def events_single_check(self):                                #Execute events in the single list and remove the event from it
        for e in self.eventsSingleCheck:
            e.execute()
            self.eventsSingleCheck.remove(e)

__STATICEVENTHANDLER = __EventHandler()

def get_static_manager():
    global __STATICEVENTHANDLER
    if __STATICEVENTHANDLER is None:
        try:
            __STATICEVENTHANDLER = __EventHandler()
        except Exception as e:
            raise TypeError from e
    return __STATICEVENTHANDLER
    