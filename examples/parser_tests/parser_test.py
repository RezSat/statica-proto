import os
import sys

folder_to_add = os.path.abspath(r'C:\Users\Administrator\Documents\statica-proto') 
sys.path.insert(0, folder_to_add)

from statica.parsing import Parser

source = open(r'C:\Users\Administrator\Documents\statica-proto\examples\example.sta', 'r').read()

parser = Parser()
ast = parser.parse(source)
print(ast)