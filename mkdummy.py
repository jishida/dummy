#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys, os, getpass, hashlib
from os import path

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        file = '.dummy/dummyfile'
    file = None
    size = None
    argv = sys.argv[1:]
    while len(argv) > 0:
        arg = argv.pop(0)
        try:
            if arg in ('-s', '--size',):
                if size or len(argv) == 0:
                    raise Exception()
                size = int(argv.pop(0))
                if size < 1:
                    raise Exception()
            else:
                if file:
                    raise Exception()
                file = arg
        except:
            print('invalid arguments', file=sys.stderr)
            sys.exit(1)
    if not file:
        file = '.dummy/dummy'
    if not size:
        size = 65536

    file = path.abspath(file)
    print('generate "%s"' % file, file=sys.stderr)
    dir = path.dirname(file)

    if path.exists(file):
        while True:
            print('%s already exists. overwrite it? (y/n)' % file, file=sys.stderr)
            if sys.version_info[0] == 2:
                yn = raw_input()
            else:
                yn = input()
            if yn == 'y':
                break
            elif yn == 'n':
                sys.exit(1)
    elif not path.isdir(dir):
        os.makedirs(dir)

    seed = getpass.getpass('seed: ')
    seed2 = getpass.getpass('confirm seed: ')
    if seed != seed2:
        print('seed mismatch', file=sys.stderr)
        sys.exit(1)
    if sys.version_info[0] != 2:
        seed = seed.encode()
    
    pos = 0
    with open(file, 'wb') as f:
        while True:
            seed = hashlib.sha256(seed).digest()
            if len(seed) + pos >= size:
                f.write(seed[:size - pos])
                break
            else:
                f.write(seed)
                pos += len(seed)
