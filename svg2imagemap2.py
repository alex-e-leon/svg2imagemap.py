#!/usr/local/bin/python

"""
Author:Alex Leon
This script converts a subset of SVG into an HTML imagemap

Note *subset*.  It only handles <path> elements, for which it only pays
attention to the start and endpoints.  Futher, it doesnt notice any transforms.

It was based off of a script written by david lynch (davidlynch.org)
and stripped down to remove his groups, and transform support but to use svg.paths
svg parsing (and support a much more robust subset of SVG syntax)

It takes several possible arguments, in the form:
$ svn2imagemap.py FILENAME [x y]

FILENAME must be the name of an SVG file.  All other arguments are optional.

x and y, if present, are the dimensions of the image you'll be creating from
the SVG.  If not present, it assumes the values of the width and height
attributes in the SVG file.
"""

import os
import re
import sys
import xml.dom.minidom
from svg.path import parse_path
 
if not( len(sys.argv) == 2 or len(sys.argv) == 4 ):
    sys.exit("svn2imagemap.py FILENAME [x y]")
if not os.path.exists(sys.argv[1]):
    sys.exit("Input file does not exist")
x, y, groups = None, None, None
if len(sys.argv) == 4:
    x = float(sys.argv[2])
    y = float(sys.argv[3])

svg_file = xml.dom.minidom.parse(sys.argv[1])
svg = svg_file.getElementsByTagName('svg')[0]

raw_width = float(svg.getAttribute('width'))
raw_height = float(svg.getAttribute('height'))
width_ratio = x and (x / raw_width) or 1
height_ratio = y and (y / raw_height) or 1

elements = svg.getElementsByTagName('path')

def get_points(path):
    path = parse_path(path)
    points = []
    for p in path:
        points.append([p.start.real, p.start.imag])
        points.append([p.end.real, p.end.imag])
    return points 

paths = []
for e in elements:
    path = get_points(e.getAttribute('d'))
    last_point = path[0]
    condensed_path = [last_point]
    for p in path:
        if p != last_point:
            condensed_path.append(p)
        last_point = p
        
    paths.append(condensed_path)
    

out = []
for path in paths:
    out.append('<area href="#" shape="poly" coords="%s"></area>' %
        (', '.join([ ("%d,%d" % (p[0]*width_ratio, p[1]*height_ratio)) for p in path ]))
        )

outfile = open(sys.argv[1].replace('.svg', '.html'), 'w')
outfile.write('\n'.join(out))
