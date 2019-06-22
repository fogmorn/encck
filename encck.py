#!/usr/bin/env python
# -*- coding: utf-8 -*-

# encck - pre-commit git hook that checks encoding for each 
# pre-commited file.
#
# Rename this script as `pre-commit' put it into .git/hooks dir of your 
# project and make it executable.
#
# It will be executed before git commit command.
#
# By default only `*.sql' files are checked. You may specify your extension 
# of files that you want to check in `ENC' variable.

import re
import sys
import os.path
from subprocess import Popen, PIPE


def file_ck(f,ENC):
    with open(f, 'rb') as fh:
        print "encck: Handling file: %s" % f
        # line number in file (if error occurs)
        nl = 1

        for line in fh:
            # rstrip - strip linebreaks
            line = line.rstrip()

            # exclude SQL comment lines
            if line.startswith('--'):
                line = str(next(fh, None)).rstrip()
                nl+=1

            # exclude SQL comment multilines
            if line.startswith('/*'):
                while not line.endswith('*/'):
                    line = str(next(fh, None)).rstrip()
                    nl+=1
                line = str(next(fh, None)).rstrip()
                nl+=1

            enc_ck(line,nl,ENC)
            has_cyrillic(line,nl)

            nl+=1
    fh.close()
    print "\n"
    return


def has_cyrillic(line,nl):
    # checks for cyrillic alphabet
    if bool(re.search('[А-Яа-я]', line)):
        err_found(nl,e='Cyrillic symbols.')
    return


def enc_ck(line,nl,ENC):
    # checks for unicode accordance
    try:
        line.decode(ENC)
    except Exception as e:
        err_found(nl,e)
    return


def err_found(nl,e=False):
    print "encck: Error in line %s:" % nl
    if e: print "encck:   %s\n" % e

    global wrong_encoding
    wrong_encoding = True

    return


if __name__=="__main__":
    ENC = "utf-8" # encoding for checking
    EXT = "sql"   # file extension that should be check out

    # get list of pre-commited files using git cli
    p = Popen(['git', 'diff-index', '--cached', 'HEAD', '--name-only'],
                stdin=PIPE, stdout=PIPE, stderr=PIPE)

    output, err = p.communicate("stdin")
    if not err:
        # building list of files (output is list in column)
        files = output.rstrip().split('\n')
    else:
        print err
        sys.exit(1)

    if not files[0]:
        print "encck: Nothing to do. Exit."
        sys.exit(0)

    global wrong_encoding
    wrong_encoding = False

    for f in files:
        # check for file extension
        if not EXT in os.path.splitext(f)[-1]:
            continue

        if os.path.isfile(f):
            # check file enconding
            file_ck(f,ENC)
        else:
            print "encck: Skip file. File is absent, maybe it was deleted: %s" % f


    if wrong_encoding:
        # if wrong enc detected - git doesn't pass further
        print "encck: Wrong encoding. Can't perform commit operation"
        sys.exit(1)
