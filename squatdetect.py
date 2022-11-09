#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detect packages which might have been typosquatted based on string similarity
level calculated from a dataset of popular packages.
It can be coupled with a shell alias/function for pip/pip3 to prevent installing
typosquatted packages. No magic, just stdlib :)

For example:

function pip3 {
~/.local/bin/squatdetect.py --packages "${@: -1}" | grep 'might be impersonating' && return
$(which pip3) "$@"
}
"""

import argparse
from difflib import SequenceMatcher
import json
import pkg_resources

parser = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--type', help='Package type', default='pip',
                    nargs='?', choices=['pip'])
parser.add_argument('--packages', help='Package(s) to check, \
                    if no packages are specified, all installed packages will be checked',
                    required=False, nargs='+')
parser.add_argument('--confidence', help='Level of confidence to be set. Default: 7',
                    type=int, choices=range(1, 10), default=7)
args = parser.parse_args()

if args.type == 'pip':
    with open("pip.json", encoding='UTF-8') as source:
        data=json.loads(source.read())
    package_names = [_['project'] for _ in data['packages']]

if args.packages:
    packages_to_check = args.packages
else:
    print('Checking all installed packages ..')
    packages_to_check = [_.key for _ in pkg_resources.working_set]

for p in package_names:
    for package in packages_to_check:
        if not package in package_names:
            similarity = SequenceMatcher(None, p, package).ratio()
            if similarity > args.confidence/10:
                print("**%s** might be impersonating %s (%f%% similar)" %
                     (package, p, similarity*100))
