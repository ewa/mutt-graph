#!/usr/bin/env python

import sys
import os
import networkx as nx
import re

def pathfix(p):
    pwd = os.getcwd()
    full_pwd = os.path.realpath(os.path.abspath(os.path.expanduser(pwd)))
    full_p = os.path.realpath(os.path.abspath(os.path.expanduser(p)))

    if full_p.startswith(full_pwd):
        #Make it relative
        return os.path.relpath(full_p,full_pwd)
    #print full_p, full_pwd
    else:
        return full_p

def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.

    From ToolMakerSteve on StackOverflow: http://stackoverflow.com/a/20577580
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

def proc_source_simple(sfname, tname, why, G):
    #Str
    tname = dequote(tname)
    tfile = pathfix(tname)
    G.add_edge(sfname, tfile, why=why)
    #print sfname, tfile

def proc_source_pathlist(sfname, tname, why, G):
    #Str
    tname = dequote(tname)
    tlist = tname.split(':')
#    tlist = [os.path.abspath(f) for f in tlist]
    for f in tlist:
        proc_source_simple(sfname, f, why, G)



def add_edges(f,G):
    src_pat = re.compile(r"^\s*source\s+(\S+)")    ## Source command
    # UGLY: These are all exactly the same except for the variable name
    alias_pat = re.compile(r"^\s*set\s*alias_file\s*=\s*(\S+)")
    cert_pat = re.compile(r"^\s*set\s*certificate_file\s*=\s*(\S+)")
    sig_pat = re.compile(r"^\s*set\s*signature\s*=\s*(\S+)")
    mailcap_pat = re.compile(r"^\s*set\s*mailcap_path\s*=\s*(\S+)")
    
    things_to_look_for = [
        ##RE,      grp,  func to call,         why
        (src_pat,     1, proc_source_simple,   "source"),
        (alias_pat,   1, proc_source_simple,   "alias_file"),
        (cert_pat,    1, proc_source_simple,   "certificate_file"),
        (sig_pat,     1, proc_source_simple,   "signature"),
        (mailcap_pat, 1, proc_source_pathlist, "mailcap_path")]
         

    for i, line in enumerate(open(f)):
        for (pat, grpnum, fun, why) in things_to_look_for:
            for match in re.finditer(pat, line):
                fun(f, match.group(grpnum), why, G)
                

def main (args):
    files = args
    files = [pathfix(f) for f in files]
    
    G = nx.DiGraph()
    for f in files:
        G.add_node(f)

    for f in files:
        add_edges(f,G)

    A=nx.to_agraph(G)
    A.draw('foo.pdf', prog="dot")
        

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
