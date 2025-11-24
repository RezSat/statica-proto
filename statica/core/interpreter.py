"""
Interpreter
After validated AST this can be used to execute the source with the comands.
Takes AST, Context

There might be a better way to do visiting with builtins
from Lark, but I don't really get the documentation therefore
I willl stick with what i understood at the moment.
Feel free to optimize.
"""

import logging
import os
from lark import visitors
import pandas as pd
from tabulate import tabulate

from statica.core.exceptions import RuntimeError
from statica.core.context import Context



logger = logging.getLogger(__name__)

class Interpreter(visitors.Interpreter):
    def __init__(self, context: Context):
        self.context = context

    def interpret(self, ast):
        for tree in ast:
            self.visit(tree)

    def statement(self, tree):
        current_child = tree.children[0]
        stmt_type = current_child['cmd']

        if stmt_type == 'assign':
            var_name = current_child['name']
            expr = current_child['expr']
            self.assign(var_name, expr)
        if stmt_type == 'describe':
            # later maybe describe can handle more than just a dataset.
            self.describe_stmt(current_child['dataset'])

    def assign(self, var_name, expr):
        loaded_data = self.load_stmt(file=expr['file'], header=expr['header'])
        self.context.set_var(var_name, loaded_data)

    def load_stmt(self, file: str, header:bool):
        # move this into a single utility function
        # used in the interpreter and validator
        data = None
        base_dir = self.context.base_dir
        full_path = os.path.join(base_dir, file)
        # later add support for additional files and 
        # methods to try handling unknown formats with "tried-our-best" approach.:)
        data = pd.read_csv(full_path, header=0 if header else "infer") # code-snippet from the original codebase
        return data
    
    def describe_stmt(self, var_name):
        #decribe the dataset with freq, mean, min, max like basic pandas describe stuff.
        #future maybe add a feature to show in a gui as well instead of just printing to the console.
        df = self.context.get_var(var_name)
        # code-snippet from the original codebase
        desc = df.describe(include='all').T.reset_index()
        print(tabulate(desc, headers="keys", tablefmt="github", showindex=False))
