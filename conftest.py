from os import environ
from datetime import datetime
from inspect import cleandoc
import json
import re


def pytest_configure(config):
    config.pluginmanager.register(JSONPlugin(config))


class JSONPlugin:
    def __init__(self, config):
        self._report = {}

    def pytest_runtest_makereport(self, item, call):
        self._class_docstring = cleandoc(item.parent.obj.__doc__)
        self._test_docstring = cleandoc(item.obj.__doc__)
        # import pdb; pdb.set_trace()

    def pytest_runtest_logreport(self, report):
        if report.when != 'call':
            return
        json_output = {
            'desc': self._test_docstring,
            'args': re.findall(r'\[([^]]*)\]', report.head_line),
            'outcome': report.outcome,
            'error_msg': report.longreprtext,
        }

        module_name = re.match(r'tests/test_([^.]+)\.py',
                               report.fspath).group(1)

        if module_name not in self._report:
            class_desc = self._class_docstring[5:]
            class_desc = class_desc[0].upper() + class_desc[1:]
            self._report[module_name] = {
                'desc': class_desc,
                'results': {},
            }
        self._report[module_name]['results'][report.head_line] = json_output

    def pytest_sessionfinish(self, session):
        overall_status = 'healthy'
        for v in self._report.values():
            total = len(v['results'])
            passed = len([x for x in v['results'].values()
                          if x['outcome'] == 'passed'])
            v['status'] = 'healthy' if total == passed else 'unhealthy'
            if v['status'] == 'unhealthy':
                overall_status = 'unhealthy'
        report = {
            'created_at': str(datetime.utcnow()),
            'build': environ.get('TRAVIS_BUILD_NUMBER'),
            'status': overall_status,
            'report': self._report,
        }

        with open('report.json', 'w') as f:
            json.dump(report, f)
