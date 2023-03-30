from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json
from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import normpath

import execnet

import scanbackend

"""
This is a module designed to be called from Python 2 or 3 and is the client
side. See scanbackend for the back server module that runs on Python 2 and runs
effectively scancode.
"""


def scan(locations, deserialize=False, scancode_root_dir=None):
    """
    Scan the list of paths at `location` and return the results as an iterable
    of JSON strings. If `deserialize` is True the iterable contains a python data
    instead.
    Each location is scanned independently.
    """
    if not scancode_root_dir:
        scancode_root_dir = abspath(normpath(__file__))
        scancode_root_dir = dirname(dirname(dirname(scancode_root_dir)))
    python = join(scancode_root_dir,'sushant', 'env_scancode', 'bin', 'python')
    spec = 'popen//python={python}'.format(**locals())
    gateway = execnet.makegateway(spec)  # NOQA
    channel = gateway.remote_exec(scanbackend)

    for location in locations:
        # build a mapping of options to use for this scan
        scan_kwargs = dict(
            location=location,
            license=True,
            license_text=True,
            license_diag=True,
            copyright=True,
            info=True,
            processes=0,
        )

        channel.send(scan_kwargs)  # execute func-call remotely
        results = channel.receive()
        if deserialize:
            results = json.loads(results)
        yield results


if __name__ == '__main__':
    import sys  # NOQA
    args = sys.argv[1:]
    for s in scan(args):
        print(s)