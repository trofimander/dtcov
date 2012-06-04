import sys
from coverage.collector import PyTracer
from dtcov.dt_django import DjangoTemplateFrame

import inspect
from dtcov.dt_file_utils import DictContains
import traceback

def inherits(cls, *names):
    if cls.__name__ in names:
        return True
    inherits_node = False
    for base in inspect.getmro(cls):
        if base.__name__ in names:
            inherits_node = True
            break
    return inherits_node


def is_django_render_call(frame):
    try:
        name = frame.f_code.co_name
        if name != 'render':
            return False

        if not DictContains(frame.f_locals, 'self'):
            return False

        cls = frame.f_locals['self'].__class__

        inherits_node = inherits(cls, 'Node')

        if not inherits_node:
            return False

        clsname = cls.__name__
        return clsname != 'TextNode' and clsname != 'NodeList'
    except:
        traceback.print_exc()
        return False


def is_django_context_get_call(frame):
    try:
        if not DictContains(frame.f_locals, 'self'):
            return False

        cls = frame.f_locals['self'].__class__

        return inherits(cls, 'BaseContext')
    except:
        traceback.print_exc()
        return False


def is_django_resolve_call(frame):
    try:
        name = frame.f_code.co_name
        if name != '_resolve_lookup':
            return False

        if not DictContains(frame.f_locals, 'self'):
            return False

        cls = frame.f_locals['self'].__class__

        clsname = cls.__name__
        return clsname == 'Variable'
    except:
        traceback.print_exc()
        return False




def find_django_render_frame(frame):
    while frame is not None and not is_django_render_call(frame):
        frame = frame.f_back

    return frame

stopping = False

class DjangoTemplateTracer(PyTracer):
    def __init__(self):
        super(DjangoTemplateTracer, self).__init__()
        self.cur_django_file_data = None

    def _trace(self, frame, event, arg_unused):
        super(DjangoTemplateTracer, self)._trace(frame, event, arg_unused)

        try:
            if event == 'call' and is_django_render_call(frame):
                frame = DjangoTemplateFrame(frame)

                filename = frame.f_code.co_filename
    #            print("File name %s"%filename)
    #            tracename = self.should_trace_cache.get(filename)
    #            if tracename is None:
    #                tracename = self.should_trace(filename, frame)
    #                self.should_trace_cache[filename] = tracename
    #                print("called, stack is %d deep, tracename is %r" % (
    #                           len(self.data_stack), tracename))
                tracename = filename
                if tracename:
                    if tracename not in self.data:
                        self.data[tracename] = {}
                    self.cur_django_file_data = self.data[tracename]

                    if self.arcs:
    #                    print("lin", self.last_line, frame.f_lineno)
                        self.cur_django_file_data[(self.last_line, frame.f_lineno)] = None
                    else:
    #                    print("lin", frame.f_lineno)
                        self.cur_django_file_data[frame.f_lineno] = None
        except :
            traceback.print_exc()

        return self._trace

    def start(self):
        sys.settrace(self._trace)
        return self._trace

    def stop(self):
        """Stop this Tracer."""
        if stopping:
            return
        if hasattr(sys, "gettrace") and self.warn:
            if sys.gettrace() != self._trace:
                msg = "Trace function changed, measurement is likely wrong: %r"
                self.warn(msg % sys.gettrace())
        sys.settrace(None)
        global stopping
        stopping = True

    def get_stats(self):
        """Return a dictionary of statistics, or None."""
        return None