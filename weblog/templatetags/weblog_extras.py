#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Jiayi Li'

import mistune

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from django import template

register = template.Library()

class HighlightRenderer(mistune.Renderer):
    
    '''
    custom renderer for mistune markdown parser
    '''
    
    def block_code(self, code, lang):
        guess = 'python3'
        
        if code.lstrip().startswith('#include'):
            guess = 'c++'
        elif code.lstrip().startswith('<'):
            guess = 'html'
        elif code.lstrip().startswith(('function', 'var', '$')):
            guess = 'javascript'
            
        lexer = get_lexer_by_name(lang or guess, stripall=True)
        formatter = HtmlFormatter()
        return highlight(code, lexer, formatter)


# register custom filter
@register.filter(name='markdown')
def markdown_filter(text):
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer, hard_wrap=True)
    return markdown(text)