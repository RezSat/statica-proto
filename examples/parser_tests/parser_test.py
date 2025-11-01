import os
import sys

folder_to_add = os.path.abspath(r'C:\Users\Administrator\Documents\statica-proto') 
sys.path.insert(0, folder_to_add)

from statica.parsing import Parser
from statica.parsing import ASTValidator
from statica.core import Context

source = open(r'C:\Users\Administrator\Documents\statica-proto\examples\parser_tests\test1.sta', 'r').read()

parser = Parser()
context = Context()
ast = parser.parse(source)
#print(ast)
validator = ASTValidator(context)
validated_ast = validator.validate(ast)
print(validated_ast)