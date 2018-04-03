# !/usr/bin/python
# -*- coding: utf-8 -*-
'''
 * Copyright (c) 2015 Spotify AB.
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
'''
import argparse
import os
import subprocess


def _find_name_from_blame(blame_line):
    """
    Finds the name of the committer of code given a blame line from git

    Args:
        blame_line: A string from the git output of the blame for a file.
    Returns:
        The username as a string of the user to blame
    """
    blame_info = blame_line[blame_line.find('(')+1:]
    blame_info = blame_info[:blame_info.find(')')]
    blame_components = blame_info.split()
    name_components = blame_components[:len(blame_components)-4]
    return ' '.join(name_components)

def _find_java_tests(blame_lines, names):
    """
    Finds the number of Java test cases per user. This will find tests both
    with the @Test annotation and the standard test methods.

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
        names: The current dictionary containing the usernames as a key and the
        number of tests as a value.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.
    """
    next_is_test = False
    counter = 0
    next_is_test_statement = False
    test_name = ""
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_with_spaces = blame_code_nospaces
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if blame_code_nospaces.startswith('}') and next_is_test_statement:
            next_is_test_statement = False
            print "Test %(n)s has %(i)d lines." % {'n': test_name,'i': counter }
            counter = 0
        if next_is_test_statement:
            counter += 1
        if next_is_test or blame_code_nospaces.startswith('publicvoidtest'):
            test_name = _get_test_name(blame_code_with_spaces)
            next_is_test_statement = True
            
            name = _find_name_from_blame(blame_line)
            name_count = names.get(name, 0)
            names[name] = name_count + 1
            next_is_test = False
        else:
            next_is_test = blame_code_nospaces.startswith('@Test')
    return names


def _get_test_name(blame_line):
    return [i for i in blame_line.split() if "()" in i][0][:-2]

def _find_git_status(directory):
    """
    Finds the number of tests per user within a given directory. Note that this
    will only work on the root git subdirectory, submodules will not be
    counted.

    Args:
        directory: The path to the directory to scan.
        xctestsuperclasses: An array of strings containing names for xctest
        superclasses.
    Returns:
        A dictionary built off the names argument containing the usernames as a
        key and the number of tests as a value.

    >>> _find_git_status('tests', 'SPTTestCase')
    {'Will Sackfield': 6}
    """
    names = {}
    java_extensions = ['.java']
    valid_extensions = java_extensions
    # valid_extensions.extend(python_extension)
    for root, dirs, files in os.walk(directory):
        for name in files:
            filename, fileextension = os.path.splitext(name)
            absfile = os.path.join(root, name)
            if fileextension in valid_extensions:
                try:
                    with open(absfile) as sourcefile:
                        source = sourcefile.read()
                        p = subprocess.Popen(['git', 'blame', absfile],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        print out
                        blame_lines = out.splitlines()
                        if fileextension in java_extensions:
                            names = _find_java_tests(blame_lines,
                                                     names)
                except:
                    'Could not open file: ' + absfile
    return names


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--directory',
                        help='The directory to search for files in',
                        required=False,
                        default=os.getcwd())
    parser.add_argument('-v',
                        '--version',
                        help='Prints the version of testing game',
                        required=False,
                        default=False,
                        action='store_true')
    args = parser.parse_args()
    if args.version:
        print 'testing game version 1.0.0'
        return
    names = _find_git_status(args.directory)
    total_tests = 0
    for name in names:
        total_tests += names[name]
    print "Total Tests: %(t)d" % {'t': total_tests}
    print "-------------------------------------------"
    sorted_list = sorted(names.items(), key=lambda x: x[1], reverse=True)
    for t in sorted_list:
        percentage = (float(t[1]) / float(total_tests)) * 100.0
        t_index = sorted_list.index(t) + 1
        print "%(i)d. %(n)s, %(t)d (%(p).2f%%)" % {'i': t_index,
                                                   'n': t[0],
                                                   't': t[1],
                                                   'p': percentage}

if __name__ == "__main__":
    _main()
