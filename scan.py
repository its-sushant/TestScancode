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

class scan:
    def __init__(self, locations):
        self.root_dir = abspath(normpath(__file__))
        self.root_dir = dirname(dirname(dirname(self.root_dir)))
        self.python = join(self.root_dir,'sushant', 'env_scancode', 'bin', 'python')
        self.spec = 'popen//python={self.python}'.format(**locals())
        self.gateway = execnet.makegateway(self.spec)
        self.channel = self.gateway.remote_exec(scanbackend)
        self.locations = locations

    def scanfiles(self, deserialize=False):
        """
        Scan the list of paths at `location` and return the results as an iterable
        of JSON strings. If `deserialize` is True the iterable contains a python data
        instead.
        Each location is scanned independently.
        """
        
        for location in self.locations:
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

            self.channel.send(scan_kwargs)  # execute func-call remotely
            results = self.channel.receive()
            if deserialize:
                results = json.loads(results)
            yield results

if __name__ == '__main__':
    import sys  
    args = sys.argv[1:]
    scanner = scan(args)
    for s in scanner.scanfiles():
        print(s)