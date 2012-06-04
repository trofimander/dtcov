import re
import dtcov

HELP_TOPICS = r"""

== help =======================================================================
Django Template Coverage version %(__version__)s
Measures coverage of tags and expression in rendered Django templates.

usage: dtcov <command> [options] [args]

Commands:
    combine     Combine a number of data files.
    erase       Erase previously collected coverage data.
    help        Get help on using coverage.py.
    html        Create an HTML report.
    report      Report coverage stats on modules.
    run         Run a Python program and measure code execution.
    xml         Create an XML report of coverage results.

Use "dtcov help <command>" for detailed help on any command.

For more information, see %(__url__)s

== minimum_help ===============================================================
Django Template Coverage.  Use 'dtcov help' for help.

== version ====================================================================
Django Template Coverage version %(__version__)s.  %(__url__)s

"""

def help(error=None, topic=None, parser=None):
    """Display an error message, or the named topic."""
    assert error or topic or parser
    if error:
        print(error)
        print("Use 'dtcov help' for help.")
    elif parser:
        print(parser.format_help().strip())
    else:
        # Parse out the topic we want from HELP_TOPICS
        topic_list = re.split("(?m)^=+ (\w+) =+$", HELP_TOPICS)
        topics = dict(zip(topic_list[1::2], topic_list[2::2]))
        help_msg = topics.get(topic, '').strip()
        if help_msg:
            print(help_msg % dtcov.__dict__)
        else:
            print("Don't know topic %r" % topic)