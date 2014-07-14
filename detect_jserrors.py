#!/usr/bin/env python

import os
import sys

#from collections import OrderedDict
#list(OrderedDict.fromkeys(items))


class Known(object):
    def __init__(self):
        self.interestingJsErrors = []
        self.interestingJsWarnings = []

    def read_known_file(self):
        '''
        Returns a list of known errors excluding comments.
        '''
        knownErrors = []
        with open(os.path.expanduser(os.path.join(os.pardir, os.pardir, 'known',
                                                     'mozilla-central', 'jserrors.txt')), 'rb') as f:
            contentsF = f.readlines()
            for line in contentsF:
                if not line.startswith('#'):
                    knownErrors.append(line.rstrip())

        return [x for x in knownErrors if x]

    def analyse_log_file(self):
        '''
        Analyses the log files and appends interesting lines when found.
        '''
        outfile = os.path.expanduser(os.path.join('out.txt'))
        with open(outfile, 'rb') as f:
            contentsF = f.readlines()
            for line in contentsF:
                # Gaia and Gecko problems appear here
                if 'Gecko' in line and '[' in line:
                    excludeLeftPart = line.split('[')[1]
                    errorMsg = excludeLeftPart.split(' line: ')[0]
                    if 'JavaScript error'.lower() in line.lower() and errorMsg not in str(self.read_known_file()) and line.rstrip() not in self.interestingJsErrors:
                        self.interestingJsErrors.append(line.rstrip())
                    elif 'JavaScript warning'.lower() in line.lower() and errorMsg not in str(self.read_known_file()) and line.rstrip() not in self.interestingJsWarnings:
                        self.interestingJsWarnings.append(line.rstrip())

                    for knownError in self.read_known_file():
                        if 'JavaScript error'.lower() in line.lower() and knownError in errorMsg and line.rstrip() in self.interestingJsErrors:
                            self.interestingJsErrors.remove(line.rstrip())
                        if 'JavaScript warning'.lower() in line.lower() and knownError in errorMsg and line.rstrip() in self.interestingJsWarnings:
                            self.interestingJsWarnings.remove(line.rstrip())


def main():
    kn = Known()
    kn.analyse_log_file()

    print '\n Total interesting error count: ' + str(len(kn.interestingJsErrors + kn.interestingJsWarnings))

    print '\n Interesting JavaScript error count: ' + str(len(kn.interestingJsErrors))
    for line in kn.interestingJsErrors:
        print line
    print

    print '\n Total JavaScript warning count: ' + str(len(kn.interestingJsWarnings))
    for line in kn.interestingJsWarnings:
        print line
    print


if __name__ == '__main__':
    main()
