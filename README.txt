Django Template Coverage was merged to coverage.py as a plugin: http://nedbatchelder.com/blog/201501/coveragepy_for_django_templates.html

It is recommended to use it instead of original project.

--

Django Template Coverage
Measures coverage of tags and expression in rendered Django templates.

Usage is the same as in coverage.py tool.

Collecting coverage data: dtcov run manage.py runserver --noreload 8000
Making report in console: dtcov report
Making HTML report: dtcov html
Making XML report: dtcov xml



