# This Source Code is subject to the terms of the Mozilla Public License
# version 2.0 (the "License"). You can obtain a copy of the License at
# http://mozilla.org/MPL/2.0/.

import select

class EventHandler(object):

    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True

    def fileno(self):
        return -1


class SocketEventHandler(EventHandler):
    
    def __init__(self, sock):
        EventHandler.__init__(self)
        self.sock = sock

    def close(self):
        if self.closed:
            return
        EventHandler.close(self)
        if self.sock:
            self.sock.close()
            self.sock = None

    def fileno(self):
        return self.sock.fileno()


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
