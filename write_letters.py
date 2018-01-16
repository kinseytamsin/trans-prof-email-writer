#!/usr/bin/env python

# Copyright (C) 2018 Kinsey Favre
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from contextlib import contextmanager

from jinja2 import Environment, FileSystemLoader
from jsonschema import validate, ValidationError
import yaml

TEMPLATE_FILE = 'letter.jinja2'
DATA_FILE = 'classes.yaml'
DATA_SCHEMA_FILE = 'schema.yaml'
DAYS_DICT = {
    'M': 'Monday',
    'T': 'Tuesday',
    'W': 'Wednesday',
    'R': 'Thursday',
    'F': 'Friday',
    'MW': 'Monday and Wednesday',
    'TR': 'Tuesday and Thursday',
    'MWF': 'Monday, Wednesday, and Friday'
}

def full_name(x): return ' '.join(x[n] for n in ('first', 'last'))
def nonlprint(*args, **kwargs): print(*args, **kwargs, end='')

@contextmanager
def progress_message(msg, ok_msg=None, err_msg=None):
    nonlprint(msg + '... ')
    try:
        yield
    except Exception as e:
        print(err_msg or 'failed')
        raise e
    else:
        print(ok_msg or 'done')

@contextmanager
def fileopen_progress_message(file, msg=None, mode='r', *args, **kwargs):
    if 'r' in mode and 'w' not in mode:
        action = 'loading'
    elif 'w' in mode:
        action = 'writing'
    with progress_message(msg or (action + ' ' + file)):
        with open(file, mode=mode, *args, **kwargs) as f:
            yield f

with fileopen_progress_message(DATA_SCHEMA_FILE, 'loading data schema') as f:
    schema = yaml.load(f)

with fileopen_progress_message(DATA_FILE) as f:
    data = yaml.load(f)

with progress_message('validating data', 'OK'):
    validate(data, schema)

for c in data['classes']:
    for m in c['meeting']:
        m['days'] = DAYS_DICT[m['days']]

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template(TEMPLATE_FILE)
render_params = {}
for key in ('chosen_name', 'dead_name', 'pronouns'):
    render_params[key] = data[key]
for key in ('chosen_name', 'dead_name'):
    render_params[key + '_full'] = full_name(data[key])

for c in data['classes']:
    for key in ('course_name', 'meeting', 'instructor'):
        render_params[key] = c[key]
    outfile = 'letter-{cid}.txt'.format(cid=c['id'])
    with fileopen_progress_message(outfile, mode='w') as f:
        f.write(template.render(render_params))
