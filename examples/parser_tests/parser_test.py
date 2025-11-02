import os
import sys

folder_to_add = os.path.abspath(r'C:\Users\Administrator\Documents\statica-proto') 
sys.path.insert(0, folder_to_add)

from statica.parsing import Parser
from statica.parsing import ASTValidator
from statica.core import Context

source_file = r'C:\Users\Administrator\Documents\statica-proto\examples\parser_tests\test1.sta'
source = open(source_file, 'r').read()

parser = Parser()
context = Context() 
context.set_base_dir(os.path.dirname(os.path.abspath(source_file)))
ast = parser.parse(source)
#print(ast)
validator = ASTValidator(context)
validated_ast = validator.validate(ast) # Non-Destructive Process (Meaning there will be no manipulation of the ast)
print(validated_ast)