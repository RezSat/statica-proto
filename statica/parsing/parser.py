"""
Parser module for Statica.

This module provides the parsing functionality for the Statica.
Ues Lark to parse the input text according to the defined grammar 
and transforms into an ASTfor execution.

The grammar is loaded from 'grammar/statica.lark' relative to this file.
"""

from lark import Lark, Transformer, Token, Tree, v_args, UnexpectedToken, UnexpectedCharacters
from pathlib import Path
from typing import List, Dict, Any, Optional
from statica.core import exceptions as ex

GRAMMAR_PATH = Path(__file__).parent / "grammar" / "statica.lark"
GRAMMAR = GRAMMAR_PATH.read_text()

class StaticaTransformer(Transformer):
    """
    Transformer to convert Lark parse tree into command dictionaries.

    This class defines methods for each grammar rule and terminal to transform
    the parse tree into a structured AST represented as lists of dictionaries.
    Each dictionary corresponds to a command with its parameters.
    """

    def NAME(self, token: Token) -> str:
        return str(token)

    def STRING(self, token: Token) -> str:
        return str(token)[1:-1]  # Strip quotes

    def NUMBER(self, token: Token) -> float:
        return float(token)

    @v_args(inline=True)
    def load_stmt(self, filename: str, header_opt: Optional[str] = None) -> Dict[str, Any]:
        return {"cmd": "load", "file": filename, "header": header_opt == "header"}

    @v_args(inline=True)
    def describe_stmt(self, dataset: str) -> Dict[str, Any]:
        return {"cmd": "describe", "dataset": dataset}

    @v_args(inline=True)
    def assign(self, name: str, expr: Any) -> Dict[str, Any]:
        return {"cmd": "assign", "name": name, "expr": expr}

    @v_args(inline=True)
    def expr_load(self, load: Dict[str, Any]) -> Dict[str, Any]:
        return load

    @v_args(inline=True)
    def expr_test(self, test: Dict[str, Any]) -> Dict[str, Any]:
        return test

    @v_args(inline=True)
    def expr_regress(self, regress: Dict[str, Any]) -> Dict[str, Any]:
        return regress

    @v_args(inline=True)
    def expr_name(self, name: str) -> str:
        return name

    @v_args(inline=True)
    def target(self, dataset: str, column: str) -> Dict[str, Any]:
        return {"dataset": dataset, "column": column}

    def test_stmt(self, items: List[Any]) -> Dict[str, Any]:
        target = items[0]
        group: Optional[str] = None
        against: Optional[float] = None
        for item in items[1:]:
            if isinstance(item, str):
                if group is None:
                    group = item
            elif isinstance(item, float):
                against = item
        return {"cmd": "ttest", "target": target, "by": group, "against": against}

    def regress_stmt(self, items: List[Any]) -> Dict[str, Any]:
        dep = items[0]
        *terms, dataset = items[1:]
        predictors = [term for term in terms]
        return {"cmd": "regress", "dep": dep, "predictors": predictors, "dataset": dataset}

    @v_args(inline=True)
    def term(self, name: str) -> str:
        return name

    def hist(self, items: List[Any]) -> Dict[str, Any]:
        bins = int(items[0]) if items else None
        return {"kind": "histogram", "bins": bins}

    def box(self, items: List[Any]) -> Dict[str, Any]:
        return {"kind": "box"}

    def scatter(self, items: List[Any]) -> Dict[str, Any]:
        return {"kind": "scatter"}

    def line(self, items: List[Any]) -> Dict[str, Any]:
        return {"kind": "line"}

    def plot_stmt(self, items: List[Any]) -> Dict[str, Any]:
        x = items[0]
        if len(items) == 3:
            y = items[1]
            kind_dict = items[2]
        else:
            y = None
            kind_dict = items[1]
        return {"cmd": "plot", "x": x, "y": y, "kind": kind_dict["kind"], "bins": kind_dict.get("bins")}

    def conclude_stmt(self, items: List[Any]) -> Dict[str, Any]:
        name = items[0]
        alpha = 0.05
        if len(items) > 1 and isinstance(items[1], float):
            alpha = items[1]
        return {"cmd": "conclude", "name": name, "alpha": alpha}

    @v_args(inline=True)
    def ask_table_stmt(self, key: str) -> Dict[str, Any]:
        return {"cmd": "ask_table", "key": key}

    def start(self, statements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [stmt for stmt in statements if stmt is not None]

class Parser:
    """
    Encapsulates the Lark parser and transformer to parse DSL text into an AST.
    Created insted of using Global variable `parser = Lark(GRAMMAR, start="start", parser="lalr")`
    due to thread-safety and increased testability.
    """

    def __init__(self) -> None:
        self.lark = Lark(GRAMMAR, start="start", parser="lalr")

    def parse(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse the given language text into a list of command dictionaries.

        Args:
            text: The language program text to parse.

        Returns:
            A list of dictionaries representing the AST commands.

        Raises:
            lark.exceptions.LarkError: If parsing fails due to syntax errors.
        """
        result = None
        try:
            tree: Tree = self.lark.parse(text)
            transformer = StaticaTransformer()
            result = transformer.transform(tree)
            # Ensure result is a list of commands
            if not isinstance(result, list):
                result = [result] if result is not None else []
        except UnexpectedToken as e:
            print(ex.SyntaxError(e.token.value, e.line, e.column))
        except UnexpectedCharacters as e:
            print(ex.SyntaxError(e.token.value, e.line, e.column))
        return result