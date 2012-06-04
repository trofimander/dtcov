from coverage.misc import join_regex, NoSource
from coverage.parser import CodeParser
from coverage.results import Analysis, Numbers
import os
import sys
from django.template import Lexer, Token
from django.template.base import TOKEN_BLOCK, TOKEN_VAR
from dtcov.dt_django import read_file

class DjangoTemplateAnalysis(Analysis):
    def __init__(self, cov, code_unit):
        self.coverage = cov
        self.code_unit = code_unit

        self.filename = self.code_unit.filename
        ext = os.path.splitext(self.filename)[1]
        source = None
        if os.path.exists(self.filename):
            try:
                self.source = read_file(self.filename)
            except :
                _, err, _ = sys.exc_info()
                raise NoSource(
                    "No source for code: %r: %s" % (self.filename, err)
                )

        if self.source is None:
            raise NoSource("No source for code: %r" % self.filename)

        self.parser = DjangoTemplateCodeParser(
            text=source, filename=self.filename,
            exclude=self.coverage._exclude_regex('exclude')
        )
        self.statements, self.excluded = self.parser.parse_source()

        # Identify missing statements.
        executed = self.coverage.data.executed_lines(self.filename)
        self.missing = sorted(set(self.statements) - set(executed))

        if self.coverage.data.has_arcs():
            self.no_branch = self.parser.lines_matching(
                join_regex(self.coverage.config.partial_list),
                join_regex(self.coverage.config.partial_always_list)
            )
            n_branches = self.total_branches()
            mba = self.missing_branch_arcs()
            n_missing_branches = sum(
                [len(v) for k,v in mba.items() if k not in self.missing]
            )
        else:
            n_branches = n_missing_branches = 0
            self.no_branch = set()

        self.numbers = Numbers(
            n_files=1,
            n_statements=len(self.statements),
            n_excluded=len(self.excluded),
            n_missing=len(self.missing),
            n_branches=n_branches,
            n_missing_branches=n_missing_branches,
        )

class DjangoTemplateCodeParser(CodeParser):
    def __init__(self, text=None, filename=None, exclude=None):
        super(DjangoTemplateCodeParser, self).__init__(text, filename, exclude)

    def _get_byte_parser(self):
        return None

    def parse_source(self):
        source_lines = set()

        lexer = Lexer(self.text, "<string>")

        tokens = lexer.tokenize()

        comment = False
        for token in tokens:
            assert isinstance(token, Token)
            if token.token_type == TOKEN_BLOCK:
                if token.contents == 'comment':
                    comment = True
                    continue
                elif token.contents == 'endcomment':
                    comment = False
                    continue

            if comment:
                continue

            if token.token_type == TOKEN_BLOCK or token.token_type == TOKEN_VAR:
                if token.token_type == TOKEN_BLOCK and token.contents.startswith('end'):
                    continue

                source_lines.add(token.lineno)

        return tuple(sorted(source_lines)), ()

    def _raw_parse(self):
        pass

    def first_line(self, line):
        return line

    def arcs(self):
        return []








