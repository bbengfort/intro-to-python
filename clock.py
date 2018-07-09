#!/usr/bin/env python
# clock
# Prints out the time specially formatted
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Sat Mar 08 15:29:47 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: clock.py [] benjamin@bengfort.com $

"""
Prints out the time specially formatted
"""

##########################################################################
## Imports
##########################################################################

import sys
from datetime import datetime
from dateutil.tz import tzlocal

##########################################################################
## A Clock Printer Object
##########################################################################

class Clock(object):

    # The "default" formats. Add more formats via subclasses or in the
    # instantation of a Clock object (or just add more here).
    FORMATS = {
        "code":"%a %b %d %H:%M:%S %Y %z",
        "json":"%Y-%m-%dT%H:%M:%S.%fZ",
        "cute":"%b %d, %Y",
    }

    @classmethod
    def local_now(klass):
        return datetime.now(tzlocal())

    @classmethod
    def utc_now(klass):
        return datetime.utcnow()

    def __init__(self, formats={}):
        self.formats = self.FORMATS.copy()
        self.formats.update(formats)

    def _local_format(self, fmt):
        return Clock.local_now().strftime(fmt)

    def _utc_format(self, fmt):
        return Clock.utc_now().strftime(fmt)

    def get_stamp(self, name):
        name  = name.strip("-")
        mname = name + "_stamp"

        # Try to find method table first
        if hasattr(self, mname):
            method = getattr(self, mname)
            return method()

        # Try to use the format string with local timezone
        if name in self.formats:
            return self._local_format(self.formats[name])

        return None

    def print_stamp(self, name):
            stamp = self.get_stamp(name)
            if stamp:
                print(stamp)
            else:
                print("No stamp format for name %s" % name)

    def help_stamp(self):

        output = ["Prints a timestamp represented with a format.",
                  "",
                  "The formats are stored in a lookup table with names, that",
                  "you can pass to the function. For instance, if you pass the",
                  "following arguments, you'll get the following results:",
                  ""]

        for name in ('--code', '--json'):
            output.append("\t%s: %s" % (name, self.get_stamp(name)))

        output.append("")
        output.append("The current formats are:")
        output.append("")

        for item in self.formats.items():
            output.append("\t%s: \"%s\"" % item)
        output.append("")

        output.append("Note that the timezone will default to the system timezone unless")
        output.append("The format requires a UTC or other timezone (like JSON)")
        output.append("")

        return "\n".join(output)

    def json_stamp(self):
        return self._utc_format(self.formats['json'])

##########################################################################
## Main Method, handle inputs to program from command line
##########################################################################

if __name__ == "__main__":

    args  = sys.argv[1:]
    clock = Clock()
    for arg in args:
        clock.print_stamp(arg)
