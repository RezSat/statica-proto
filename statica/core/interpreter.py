"""
Interpreter
After validated AST this can be used to execute the source with the comands.
Takes AST, Context
"""

import logging
from lark import visitors

from statica.core.exceptions import RuntimeError
from statica.core.context import Context



logger = logging.getLogger(__name__)

class Interpreter(visitors.Interpreter):
    def __init__(self, context: Context):
        self.context = context

    def statement(self, tree):
        stmt_type = tree.children[0]['cmd']
        if stmt_type == 'assign':
            var_name = tree.children[0]['name']
            expr = tree.children[0]['expr']
            self.assign(var_name, expr)

    def assign(self, expr):
        print(expr)

    def load_stmt(self, file: str, header:bool):
        print(file, header)