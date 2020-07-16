import threading
from collections import deque


class _Message:
    def __init__(self, body, attr):
        self.body = body
        self.attributes = attr

    def __str__(self):
        d = str(self.body)
        n = len(d)
        if n > 32:
            d = d[:32] + "..."
        return "Message%s<<<%s>>>" % (str(self.attributes), d)


class _Obj:
    pass


class API:
    def __init__(self):
        self.callbacks = {}
        self.output = {}
        self.config = _Obj()
        self.test = _Obj()
        self.test.write = self._write
        self.test.read = self._read
        self.test.hasnext = self._hasnext
        self.test.exec_timers = self._exec_timers
        self.test.stop_timers = self._stop_timers
        self.timers = {}
        self.stopTimer = False
        self.logger = _Obj()
        self.logger.info = self._info
        self.logger.debug = self._debug
        self.logger.warn = self._warn
        self.logger.error = self._error

    def add_shutdown_handler(self, *args, **kwargs):
        pass

    def tick(self, time, func):
        if self.stopTimer:
            return
        else:
            func()
            thread = threading.Timer(
                float(time.replace('s', '')),
                self.tick, [time, func])
            thread.start()

    def set_port_callback(self, portnames, cb):
        self.callbacks[tuple(portnames)] = cb

    def send(self, portname, data):
        if portname not in self.output:
            self.output[portname] = deque()
        self.output[portname].appendleft(data)

    def add_timer(self, interval, func):
        self.timers[interval] = func

    def _write(self, portnames, data):
        if type(data) in (list, tuple):
            self.callbacks[tuple(portnames)](*data)
        else:
            self.callbacks[tuple(portnames)](data)

    def _exec_timers(self):
        print(self.timers)
        for key in self.timers:
            self.tick(key, self.timers[key])

    def _stop_timers(self):
        self.stopTimer = True

    def _read(self, portname):
        res = self.output[portname].pop()
        return res

    def _hasnext(self, portname):
        return len(self.output[portname]) > 0

    def _info(self, message):
        print(message)

    def _debug(self, message):
        print(message)

    def _warn(self, message):
        print(message)

    def _error(self, message):
        print(message)


api = API()
api.Message = _Message
# ///////////////////////////////////////////////////////


def test_queue_single_port():
    # operator
    api.config.batch = "5"
    ctx = {}
    ctx["agg"] = []

    def on_input(data1):
        ctx["agg"].append(data1)
        if len(ctx["agg"]) >= int(api.config.batch):
            out = json.dumps(ctx["agg"])
            ctx["agg"] = []
            api.send("output", out)

    api.set_port_callback("inp1", on_input)

    # test
    print("testing queue write/read with single port...")
    for i in range(10):
        api.test.write("inp1", "a-%d" % i)
    counter = 0
    while api.test.hasnext("output"):
        d = ["a-%d" % i for i in range(counter * 5, (counter + 1) * 5)]
        assert api.test.read("output") == json.dumps(d)
        counter += 1
    assert counter == 2
    print("done")


def test_queue_multiple_ports():
    # operator
    api.config.batch = "5"
    ctx = {}
    ctx["agg"] = []

    def on_input(data1, data2):
        ctx["agg"].append((data1, data2))
        if len(ctx["agg"]) >= int(api.config.batch):
            out = json.dumps(ctx["agg"])
            ctx["agg"] = []
            api.send("output", out)

    api.set_port_callback(["inp1", "inp2"], on_input)

    # test
    print("testing queue write/read with multiple ports...")
    for i in range(10):
        api.test.write(["inp1", "inp2"], ["a-%d" % i, "b-%d" % i])
    counter = 0
    while api.test.hasnext("output"):
        d = [
            ("a-%d" % i, "b-%d" % i)
            for i in range(counter * 5, (counter + 1) * 5)]
        assert api.test.read("output") == json.dumps(d)
        counter += 1
    assert counter == 2
    print("done")


def test_config():
    print("test config...")
    # check it works in case underlying implementation changes
    api.config.prop_a = 123
    assert api.config.prop_a == 123
    print("done")


def test_message():
    print("test message...")
    msg = api.Message("blablabla", {"a": 5})
    assert msg.body == "blablabla"
    assert msg.attributes["a"] == 5
    print("done")


if __name__ == "__main__":
    import json
    test_queue_single_port()
    test_queue_multiple_ports()
    test_message()
    test_config()
