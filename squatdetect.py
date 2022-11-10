#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Detect packages which might have been typosquatted based on string similarity
level calculated from a dataset of popular packages.
It can be coupled with a shell alias/function for pip/pip3 to prevent installing
typosquatted packages. No magic, just stdlib :)

For example:

function pip3 {
if [[ -n "$1" ]] && [[ "$1" = 'install' ]]; then
  ~/.local/bin/squatdetect.py --packages "${@: -1}" | grep 'might be impersonating' && return
fi
$(which pip3) "$@"
}

function gem {
if [[ -n "$1" ]] && [[ "$1" = 'install' ]]; then
  ~/.local/bin/squatdetect.py --packages "${@: -1}" --type gem | grep 'might be impersonating' && return
fi
$(which gem) "$@"
}
"""

import sys
import argparse
from difflib import SequenceMatcher
import json
from subprocess import Popen, PIPE
import pkg_resources

parser = argparse.ArgumentParser(description=__doc__,
                               formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--type', help='Package type. Default: pip', default='pip',
                    nargs='?', choices=['pip', 'gem'])
parser.add_argument('--packages', help='Package(s) to check, \
                    if no packages are specified, all installed packages will be checked',
                    required=False, nargs='+')
parser.add_argument('--confidence', help='Level of confidence to be set. Default: 8',
                    type=int, choices=range(1, 10), default=8)
args = parser.parse_args()

if args.type in ('pip', 'gem'):
    with open(f"{args.type}.json", encoding='UTF-8') as source:
        data=json.loads(source.read())
    package_names = [_['project'] for _ in data['packages']]

if args.packages:
    packages_to_check = args.packages
elif args.type == 'pip':
    print('Checking all installed pip qpackages ..')
    packages_to_check = [_.key for _ in pkg_resources.working_set]
elif args.type == 'gem':
    print('Checking all installed gems ..')
    with Popen(['gem', 'list', '--quiet'],
                 stdout = PIPE,
                 stderr = PIPE) as proc:
        stdout, stderr = proc.communicate()
        if stderr:
            print(stderr)
            print('Unable to get list of gems')
            sys.exit(1)
        packages_to_check = [_.split(' ')[0].strip() for _ in
                            stdout.decode('utf-8').strip().split('\n')]

for p in package_names:
    for package in packages_to_check:
        if not package in package_names:
            similarity = SequenceMatcher(None, p, package).ratio()
            if similarity > args.confidence/10:
                print(f"**{package}** might be impersonating {p} ({similarity*100}% similar)")
