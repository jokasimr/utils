#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 09:47:45 2017

@author: user
"""

def colorize(text, colors=['red', 'blue', 'green', 'yellow']):
    '''Latex colorizes the text, returns a list - join it to get a string.'''
    ct = "\textcolor{%s}{\textbf{%s}}"
    from itertools import cycle
    s = cycle(colors)
    return [ct % (next(s), c) for c in text]

def text_function(text, deltas):
    '''Raises and lowers the "characters" (can be list-elements) 
    in the given text to match the deltas.
    
    Example: 
        text_function('Hejsan alla!', 5*sin(linspace(-pi, pi, len(text)))) 
    '''
    begin = '\raisebox{0pt}[0pt][0pt]{'
    end = '}'
    middle = [' \raisebox{%sex}{%s}' % RD for RD in zip(deltas, text)]
    return [begin]+middle+[end]


from tabulate import tabulate


def array_to_table(array, *args, label='label', description='Description text', tablefmt='latex', floatfmt='.3f', **kwargs):
    return '''
\\begin{table}
\\centering
\\caption{\label{tab:%s} %s}
\\bigskip
%s
\\end{table} ''' % (label, description, tabulate(array, *args, tablefmt=tablefmt, floatfmt=floatfmt, **kwargs))