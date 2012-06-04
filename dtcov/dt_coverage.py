import coverage
from coverage.cmdline import CoverageScript
from coverage.codeunit import CodeUnit, code_unit_factory
from coverage.misc import ExceptionDuringRun, CoverageException, NotPython
import sys
import traceback
from coverage.results import Analysis
from dtcov.dt_help import help
from dtcov.dt_report import DjangoTemplateAnalysis
from dtcov.dt_tracer import DjangoTemplateTracer
import dtcov.dt_coverage

class coverage(coverage.coverage):
    def __init__(self, **kwargs):
        super(dtcov.dt_coverage.coverage, self).__init__(**kwargs)
        self.collector._trace_class = DjangoTemplateTracer

    def _analyze(self, it):
        """Analyze a single morf or code unit.

        Returns an `Analysis` object.

        """
        if not isinstance(it, CodeUnit):
            it = code_unit_factory(it, self.file_locator)[0]

        try:
            a = Analysis(self, it)
            return a
        except NotPython:
            try:
                return DjangoTemplateAnalysis(self, it)
            except :
                traceback.print_exc()


def main(argv=None):
    """The main entrypoint to Coverage.

    This is installed as the script entrypoint.

    """
    if argv is None:
        argv = sys.argv[1:]
    try:
        status = CoverageScript(_covpkg=dtcov.dt_coverage, _help_fn=help).command_line(argv)
    except ExceptionDuringRun:
        # An exception was caught while running the product code.  The
        # sys.exc_info() return tuple is packed into an ExceptionDuringRun
        # exception.
        _, err, _ = sys.exc_info()
        traceback.print_exception(*err.args)
        status = 1
    except CoverageException:
        # A controlled error inside coverage.py: print the message to the user.
        _, err, _ = sys.exc_info()
        print(err)
        status = 1
    except SystemExit:
        # The user called `sys.exit()`.  Exit with their argument, if any.
        _, err, _ = sys.exc_info()
        if err.args:
            status = err.args[0]
        else:
            status = None
    return status
