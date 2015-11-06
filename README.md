# mutt-graph
Visualize relationships between mutt config files

## Supported relationships

    source
    alias_file
    certificate_file
    signature
    mailcap_path



# Usage
This is *very dumb* right now.  It expects all the files it will process to be supplied on the command line, and interprets all paths relative to `cwd`.  Example use:

`~/.mutt $ find . -type f | xargs python ~/src/mutt-graph/mutt-graph.py`

Produces a dot-formatted graph called `foo.pdf`

