from lark import Lark, Transformer, v_args
from pathlib import Path
import statica

GRAMMAR_PATH = Path(__file__).parent / "grammar.lark"
GRAMMAR = GRAMMAR_PATH.read_text()

parser = Lark(GRAMMAR, start="start", parser="lalr")

# We'll transform the parse tree into a list of simple command dicts
class StaticaTransformer(Transformer):
    def NAME(self, token):
        return str(token)

    def STRING(self, token):
        s = str(token)
        return s[1:-1]

    def NUMBER(self, token):
        return float(token)

    def load_stmt(self, items):
        filename = items[0]
        header = False
        if len(items) > 1:
            header = True
        return {"cmd": "load", "file": filename, "header": header}

    def describe_stmt(self, items):
        return {"cmd": "describe", "dataset": items[0]}

    def assign(self, items):
        name = items[0]
        expr = items[1]
        return {"cmd": "assign", "name": name, "expr": expr}

    def expr_load(self, items):
        return items[0]

    def expr_test(self, items):
        return items[0]

    def expr_regress(self, items):
        return items[0]

    def target(self, items):
        return {"dataset": items[0], "column": items[1]}

    def test_stmt(self, items):
        # items: target, optional 'by' group name, optional 'against' number
        target = items[0]
        group = None
        against = None
        for it in items[1:]:
            if isinstance(it, (str,)):
                # group name captured as NAME string
                if group is None:
                    group = it
            else:
                # numeric => against
                against = it
        return {"cmd": "ttest", "target": target, "by": group, "against": against}

    def regress_stmt(self, items):
        # items: dep var name, term, maybe more terms..., dataset name (last)
        dep = items[0]
        *terms, dataset = items[1:]
        predictors = [t for t in terms]
        return {"cmd": "regress", "dep": dep, "predictors": predictors, "dataset": dataset}

    def hist(self, items):
        # optional bins
        if items:
            return {"kind": "histogram", "bins": int(items[0])}
        return {"kind": "histogram", "bins": None}

    def box(self, items):
        return {"kind": "box"}

    def scatter(self, items):
        return {"kind": "scatter"}

    def vs_scatter(self, items):
        # items: NAME (column to plot)
        return {"kind": "scatter"}

    def plot_stmt(self, items):
        x = items[0]
        if len(items) == 3:
            y = items[1]
            kind = items[2]["kind"]  # because hist/box/scatter returns a dict
        else:
            y = None
            kind = items[1]["kind"]

        return {"cmd": "plot", "x": x, "y": y, "kind": kind}



    def conclude_stmt(self, items):
        name = items[0]
        alpha = 0.05
        if len(items) > 1 and isinstance(items[1], float):
            alpha = items[1]
        return {"cmd": "conclude", "name": name, "alpha": alpha}

    def ask_table_stmt(self, items):
        return {"cmd": "ask_table", "key": items[0]}

def parse_program(text):
    tree = parser.parse(text)
    transformer = StaticaTransformer()
    result = transformer.transform(tree)
    
    # Return list of children (statements)
    if isinstance(result, list):
        return result
    elif hasattr(result, 'children'):
        return [c for c in result.children if c is not None]
    else:
        return [result]

