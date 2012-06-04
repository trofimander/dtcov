import unittest
import textwrap
from dtcov.dt_report import DjangoTemplateCodeParser

class ParserTest(unittest.TestCase):
    def parse_source(self, text):
        text = textwrap.dedent(text)
        cp = DjangoTemplateCodeParser(text=text, exclude="nocover")
        ret = cp.parse_source()
        return cp, ret

    def test_else_if(self):
        (cp, ret) = self.parse_source("""\
                               Test
                               {% if True %}
                               True
                               {% else %}
                               False
                               {% endif %}
                               """)
        self.assertEquals((2, 4, 6), ret[0])


    def test_text_with_braces(self):
        (cp, ret) = self.parse_source("""\
                           Test
                           {% if True %}
                           { {  } }
                           {% else %}
                            { % {
                           {% endif %}
                           %
                           }}
                           """)
        self.assertEquals((2, 4, 6), ret[0])


    def test_expressions(self):
        (cp, ret) = self.parse_source("""\
                           {{ value}}
                           text }}
                           {% if True %}
                            {{ true }}
                           {% endif %}
                           """)
        self.assertEquals((1, 3, 4, 5), ret[0])

    def test_comments(self):
        (cp, ret) = self.parse_source("""\
                           {% comment %}
                                Comment
                                {{ comment }}
                           {% endcomment %} {{ value }}
                           {% if True %}
                           True
                            {# {{ true }} and {{ false }} #}
                           {% endif %}
                           """)
        self.assertEquals((4, 5, 8), ret[0])
