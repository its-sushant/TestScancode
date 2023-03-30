from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

"""
Python2 "server side" of the scan server. In a given execnet session, this
process will hold a loaded license index and can be invoked multiple times
without the index load penalty on each call.
"""


def as_json(results, pretty=False):
    """
    Return a JSON string from a `results` data structuret.
    """
    # this is used for its ability to handle iterables as arrays.
    import simplejson

    kwargs = dict(iterable_as_array=True, encoding='utf-8')
    # if pretty:
    #     kwargs.update(dict(indent=2 * b' '))
    # else:
    #     kwargs.update(dict(separators=(b',', b':',)))
    return simplejson.dumps(results, **kwargs) + '\n'


def run_scan(location, **kwargs):
    from scancode import cli
    pretty = kwargs.pop('pretty', True)
    return as_json(cli.run_scan(location, **kwargs), pretty=pretty)


if __name__ == '__channelexec__':
    for kwargs in channel:  # NOQA
        # a mapping of kwargs or a location string
        if isinstance(kwargs, str):
            channel.send(run_scan(kwargs))  # NOQA
        elif isinstance(kwargs, dict):
            channel.send(run_scan(**kwargs))  # NOQA
        else:
            raise Exception('Unknown arguments type: ' + repr(kwargs))