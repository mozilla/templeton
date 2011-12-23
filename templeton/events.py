import select

class EventHandler(object):

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

    def fileno(self):
        return -1


class Reactor(object):

    SELECT_TIMEOUT = 0.1

    def __init__(self):
        self.event_handlers = []
        self.enabled = True

    def stop(self):
        self.enabled = False

    def register_handler(self, handler):
        self.event_handlers.append(handler)

    def unregister_handler(self, handler):
        self.event_handlers.remove(handler)
    
    def run(self):
        while self.enabled:
            try:
                fileno_map = {}
                for e in self.event_handlers:
                    if e.closed:
                        self.event_handlers.remove(e)
                    else:
                        fileno_map[e.fileno()] = e
                rlist = fileno_map.keys()
                rlist.sort()
                try:
                    rready, wready, xready = select.select(rlist, [], [],
                                                           self.SELECT_TIMEOUT)
                except select.error, e:
                    continue
                for fileno in rready:
                    fileno_map[fileno].execute()
            except KeyboardInterrupt:
                self.enabled = False
