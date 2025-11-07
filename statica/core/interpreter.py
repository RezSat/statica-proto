"""
Interpreter
After validated AST this can be used to execute the source with the comands.
Takes AST, Context
"""

import logging
from statica.core.exceptions import RuntimeError
from statica.core.context import Context


logger = logging.getLogger(__name__)

class Interpreter:
    def __init__(self, context: Context):
        self.context = context
    
    def interpret(self, ast):
        pass
    