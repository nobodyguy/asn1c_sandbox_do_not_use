#!/usr/bin/env python
# -*- coding: utf-8 -*-
# asn1-doxygen-filter is an extension to the Doxygen utility for creating
# documents from ASN.1 files
#
# Copyright 2017 OnBoard Security, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal 
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUTNOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE ANDNONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse # parse arguments
import os.path  # getting extension from file
import sys      # output and stuff
import re       # for regular expressions

## extract doxygen-tag namespace
RE_NAMESPACE = re.compile(
    r'(?<=[@]namespace\s).+', re.IGNORECASE | re.VERBOSE
    )
## extract doxygen-tag struct
RE_STRUCT = re.compile(r'(?<=[@]class\s)\w+', re.IGNORECASE | re.VERBOSE)
RE_BRIEF = re.compile(
    r'(?<=[@]brief\s).*(?=\s-{2}\s[@])', re.IGNORECASE | re.VERBOSE | re.DOTALL
    )
RE_COMMENT_BLOCK = re.compile(
    r'^-{3}\s.*(?=^[^-\*]\w)', # Ex. ---\n
    re.IGNORECASE | re.VERBOSE | re.MULTILINE | re.DOTALL
    )
RE_COMMENT_BLOCK_START = re.compile(r'^-{3}', re.VERBOSE)
RE_COMMENT = re.compile(r'^-{2}', re.IGNORECASE | re.VERBOSE)
RE_STRUCT_DEF = re.compile(r'(^\s*[\w\ ]+)\s*(::=)',
                           re.IGNORECASE | re.VERBOSE)
RE_END = re.compile(r'^END\s*')
RE_DEFINITION = re.compile(r'^\s*DEFINITIONS.*?::=')

##
# @package asn1-doxygen-filter
# @brief A Doxygen filter to document ASN.1 structures, based on a glslfilter
#        from Sebastian Schäfer
# @author Mohammad Raashid Ansari
# @date 07/11
# @version 0.1
# @copyright MIT License
# 
# @details The asn1 file is wrapped into a struct and namespace that can be set
# with doxygen-tags.
# 
# Usage:
# - asn1 file:
#   - set doxygen name for struct name -> defaults to filename
#   - set doxygen namespace for namespace (pseudo category) -> defaults to
#     Interface name
# - doxygen file:
#   - add FILE_PATTERNS: *.asn
#   - add FILTER_PATTERNS: "*.asn=asn1-doxygen-filter.py"
#   - add EXTENSION_MAPPING=.asn=C++
# latest version on <a href=
# "https://bitbucket.org/raashid_ansari/asn1-doxygen-filter">BitBucket</a>

##
# struct to consolidate all properties of a structure
# properties: comments, code, print structure
class Asn1Structure:
    ##
    # Initialize ASN.1 Structure variables
    # @param struct_name - structure name
    def __init__(self, namespace, struct_name):
        self.namespace = namespace
        self.name = struct_name
        self.comments = []
        self.code = []

    ##
    # Store comment block for this structure
    # @param comment - a list of comment lines
    def addComment(self, comment):
        self.comments.append(comment)

    ##
    # Store code block for this structure
    # @param code_line - a list of code lines
    def addCodeLine(self, code_line):
        self.code.append(code_line)

    ##
    # Print the whole structure on standard output in the order:
    # 1. Structure name (struct name)
    # 2. Comment block
    # 3. Code block
    def printStructure(self):
        # writeLine(self.name)
        # dump the file and pad it with namespace/name class information
        # 1st: namespace + struct padding, also declare everything public
        writeLine("struct " + self.name + " {\n")
        writeLine("public:\n")
        for comment in self.comments:
            writeLine(comment)
        writeLine("\n* @code{.unparsed}\n")
        for code_line in self.code:
            writeLine('* ' + code_line)
        writeLine("* @endcode\n*/\n")
        writeLine("/** @struct " + self.namespace + "::" + self.name + " */\n")
        writeLine("};\n")

##
# run regex on a single line
# @returns either a found result or None
def getRegSearchLine(string, regex):
    search = regex.search(string)
    if search is not None:
        return search.group(0)
    return None

##
# run regex on a string array
# @returns either a found result or None
def getRegSearch(txt, regex):
    for string in txt:
        search = regex.search(string)
        if search is not None:
            return search.group(0)
    return None

##
# generate a struct name from filename
# @return just the filename - no extension and no path
def generateName(filename):
    root, ext = os.path.splitext(filename)
    head, tail = os.path.split(root)
    return tail

##
# print to standard output
def writeLine(txt):
    sys.stdout.write(txt)

##
# Extract namespace for the structures
def parseNamespace(lines):
    namespace = getRegSearch(lines, RE_NAMESPACE)
    if getRegSearchLine(namespace, re.compile(r'\W')):
        namespace = re.sub(r'\W','', namespace)
    if namespace is None:
        namespace = "Ieee1609dot2SCMS"
    else: # remove namespace line from lines
        lines = [line for line in lines if getRegSearchLine(
            line, RE_NAMESPACE) is None]
    return (namespace, lines)

##
# Extract struct name from each structure
def parseStructNames(namespace, lines):
    struct_objs = []
    for line in lines:
        struct_name = getRegSearchLine(line, RE_STRUCT)
        if struct_name is not None:
            #remove struct_name line from lines
            lines = [line for line in lines if getRegSearchLine(
                line, RE_STRUCT) is None]
            struct_objs.append(Asn1Structure(namespace, struct_name))
    return (struct_objs, lines)

##
# Extract comments for each structure
def parseComments(struct_objs, lines):
    struct_index = 0
    for i, line in enumerate(lines):
        comment_start = getRegSearchLine(line, RE_COMMENT_BLOCK_START)
        # print('LINE: ', line)
        if comment_start is not None:
            # print('COMMENT START: ', comment_start)
            comment_start = re.sub('^-{3}', '/**\n', comment_start)
            struct_objs[struct_index].addComment(comment_start)
            lines.pop(i) # remove line with "---" out of "lines" list
            # Parse until reaching end of comment block
            while getRegSearchLine(lines[i], RE_STRUCT_DEF) is None and lines:
                comment = lines.pop(i)
                comment = re.sub('-{2}', '*', comment)
                struct_objs[struct_index].addComment(comment)
            struct_index += 1
    return (struct_objs, lines)

##
# Extract code blocks for each structure
def parseCodeBlocks(struct_objs, lines):
    struct_index = 0
    for i, line in enumerate(lines):
        code_start = RE_STRUCT_DEF.search(lines[i])
        # print('CODE: ', code_start)
        if code_start is not None:
            if getRegSearchLine(code_start.group(0), RE_DEFINITION) is not None:
                # print('DEFINITION: ', code_start.group(0))
                continue
            while True:
                code = lines.pop(i)
                # print('CODE: ', code)
                struct_objs[struct_index].addCodeLine(code)
                if i:
                    if (
                        getRegSearchLine(lines[i+1], RE_END) is not None or
                        getRegSearchLine(lines[i+1], RE_COMMENT_BLOCK_START) is not None or
                        # getRegSearchLine(lines[i+1], RE_COMMENT) is not None or
                        getRegSearchLine(lines[i+1], RE_STRUCT_DEF) is not None
                    ):
                        break
            struct_index += 1
    return (struct_objs, lines)

##
# Extract the "END" of structure
def parseEnd(lines):
    end = getRegSearch(lines, RE_END)
    if end:
        lines = [x for x in lines if getRegSearchLine(x, RE_END) is None]
    return (end, lines)

##
# parse an asn file and generate needed information along on the way
# if comments contain a namespace move it the struct_name
def parseAsn(lines):
    namespace, lines = parseNamespace(lines)
    struct_objs, lines = parseStructNames(namespace, lines)
    struct_objs, lines = parseComments(struct_objs, lines)
    struct_objs, lines = parseCodeBlocks(struct_objs, lines)
    end, lines = parseEnd(lines)
    # Print to standard output
    for line in lines:
        writeLine(line)
    writeLine("namespace " + namespace + " {\n")
    for struct_obj in struct_objs:
        struct_obj.printStructure()
    writeLine("}\n")
    writeLine(end)

##
# @returns the complete file content as an array of lines
def readFile(file_name):
    FILE = open(file_name)
    file_content = FILE.readlines()
    FILE.close()
    return file_content

##
# dump all lines to stdout
def showLines(lines):
    for line in lines:
        sys.stdout.write(line)

##
# main method to open a file and parse accordingly
def filter(file_name):
    try:
        root, ext = os.path.splitext(file_name)
        lines = readFile(file_name)
        if ext.lower() == ".asn":
            parseAsn(lines)
        else:
            showLines(lines)
    except IOError as e:
        sys.stderr.write(e[1]+"\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", help="name of the file to be processed")
    args = parser.parse_args()
    filter(args.file_name)

if __name__ == '__main__':
    main()
