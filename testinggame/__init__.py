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
import numpy as np
import random
import json

def _find_java_tests(blame_lines):
    """
    Finds the number of Java test cases per user. This will find tests both
    with the @Test annotation and the standard test methods.

    Args:
        blame_lines: An array where each index is a string containing the git
        blame line.
    Returns:
        A dictionary built off the test class containing the test method name as a
        key and the number of lines as a value.
    """
    next_is_test = False
    counter = 0
    next_is_test_statement = False
    test_name = ""
    improved_current_tests = []
    code = []
    blocks = 0
    for blame_line in blame_lines:
        separator = blame_line.find(')')
        blame_code_nospaces = blame_line[separator+1:]
        blame_code_with_spaces = blame_code_nospaces
        blame_code_nospaces = blame_code_nospaces.replace(' ', '')
        blame_code_nospaces = blame_code_nospaces.replace('\t', '')
        if '{' in blame_code_nospaces:
            blocks += 1
        if '}' in blame_code_nospaces:
            blocks -= 1
        if blocks == 0 and next_is_test_statement:
            next_is_test_statement = False
            code.append(blame_code_with_spaces)
            improved_current_tests.append({ "method": test_name, "loc": counter, "code": code })
            code = []
            counter = 0
        if next_is_test_statement:
            counter += 1
            code.append(blame_code_with_spaces)
        if next_is_test or blame_code_nospaces.startswith('publicvoidtest'):
            test_name = _get_test_name(blame_code_with_spaces)
            code.append(blame_code_with_spaces)
            next_is_test_statement = True
            next_is_test = False
        else:
            next_is_test = blame_code_nospaces.startswith('@Test')
    return improved_current_tests

def _get_test_name(blame_line):
    return [i for i in blame_line.split() if "()" in i][0][:-2]

def _find_git_status(directory):
    """
    Finds the number of tests per user within a given directory. Note that this
    will only work on the root git subdirectory, submodules will not be
    counted.

    Args:
        directory: The path to the directory to scan.
    Returns:
        A dictionary built off the directory argument containing the class file as a
        key and dictionary, with the test method as the key and the LOC as a value, as a value.
    """
    tests = {}
    improved_tests = []
    java_extensions = ['.java']
    valid_extensions = java_extensions
    for root, dirs, files in os.walk(directory):
        for name in files:
            filename, fileextension = os.path.splitext(name)
            absfile = os.path.join(root, name)
            if fileextension in valid_extensions and ("test" in absfile or "Test" in absfile):
                try:
                    with open(absfile) as sourcefile:
                        source = sourcefile.read()
                        p = subprocess.Popen(['git', 'blame', absfile],
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                        out, err = p.communicate()
                        blame_lines = out.splitlines()
                        if fileextension in java_extensions:
                            current_tests = _find_java_tests(blame_lines)
                            if current_tests:
                                improved_tests.append({ 'class': filename, 'testmethods': current_tests })
                                tests[filename] = current_tests
                except:
                    'Could not open file: ' + absfile
    return improved_tests

def _write_to_file(data, project_name, save_path):
    file_name = 'data'
    if project_name:
        file_name = project_name
    with open(save_path + file_name + '.json', 'w') as fp:
        json.dump(data, fp)
        fp.close()

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
    parser.add_argument('-s',
                        '--save',
                        help='Where to save the resulting json file',
                        required=False,
                        default='')
    parser.add_argument('-g',
                        '--gitrepo',
                        help='The https link to the git repository to clone. If no link was provided, the current directory will be used.',
                        required=False,
                        default="")
    args = parser.parse_args()
    if args.version:
        print 'testing game version 1.0.0'
        return
    project_name = ''
    if args.gitrepo:
        project_name = args.gitrepo.split("/")[-1].replace('.git','')
    tests = _find_git_status(args.directory)
    _write_to_file(tests, project_name, args.save)
    total_tests = 0
    for test_class in tests:
        total_tests += len(test_class['testmethods'])
    print "Total Tests: %(t)d" % {'t': total_tests}
    print "-------------------------------------------"
    flattened_list = []
    for test_class in tests:
        print "- %(t)s" % { 't': test_class['class'] }
        for test_method in test_class['testmethods']:
            test_LOC = test_method['loc']
            flattened_list.append({ 'loc': test_LOC,
                                    'class': test_class,
                                    'method': test_method })
            print "    - %(c)d lines in %(m)s." % { 'c': test_LOC,
                                                    'm': test_method['method']}

if __name__ == "__main__":
    _main()
