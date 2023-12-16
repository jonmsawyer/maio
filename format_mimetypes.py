'''
File: format_mimetypes.py

Module: ``maio.format_mimetypes``
'''

from __future__ import annotations

from pprint import pprint

def main(filename: str):
    '''Main function.'''
    with open(filename, 'r') as fh:
        buf = fh.read()

    mimetypes = []

    lines = buf.split('\n')
    for line in lines:
        line = line.strip()
        print(f'Line: {line}')
        parts = line.split()
        print(f'Parts: {parts}')
        try:
            mimetypes.append((parts[0], ' '.join(parts[1:])))
        except IndexError:
            continue

    pprint(mimetypes)

if __name__ == '__main__':
    main('data/mime.types')
