import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from tabulate import tabulate
from .nlg import generate_conclusion, ask_user_for_table
from typing import Dict, Any


class Runtime:
    def __init__(self):
        self.env: Dict[str, Any] = {}
        self.user_tables: Dict[str, Any] = {}

    def execute(self, commands):
        # Ensure commands are dicts, not Tree objects
        for cmd in commands:
            if hasattr(cmd, 'data') and hasattr(cmd, 'children'):
                cmd = cmd.children[0] if cmd.children else {}
            if not isinstance(cmd, dict) or 'cmd' not in cmd:
                print("Invalid command:", cmd)
                continue

            c = cmd.get("cmd")
            if c == "load":
                self._cmd_load(cmd)
            elif c == "describe":
                self._cmd_describe(cmd)
            elif c == "assign":
                self._cmd_assign(cmd)
            elif c == "ttest":
                self._cmd_ttest(cmd)
            elif c == "regress":
                self._cmd_regress(cmd)
            elif c == "plot":
                self._cmd_plot(cmd)
            elif c == "conclude":
                self._cmd_conclude(cmd)
            elif c == "ask_table":
                self._cmd_ask_table(cmd)
            else:
                print("Unknown command:", cmd)

    def _cmd_load(self, cmd):
        fname = cmd["file"]
        header = cmd.get("header", False)
        try:
            df = pd.read_csv(fname, header=0 if header else 'infer')
            varname = fname.split("/")[-1].split(".")[0]
            self.env[varname] = df
            print(f"[Loaded '{fname}' into env as '{varname}' — {len(df)} rows x {len(df.columns)} cols]")
        except Exception as e:
            print("Error loading file:", e)

    def _cmd_describe(self, cmd):
        name = cmd["dataset"]
        df = self.env.get(name)
        if df is None:
            print(f"[describe] Unknown dataset '{name}'")
            return
        desc = df.describe(include='all').T.reset_index()
        print(tabulate(desc, headers="keys", tablefmt="github", showindex=False))

    def _cmd_assign(self, cmd):
        name = cmd["name"]
        expr = cmd["expr"]
        if isinstance(expr, dict) and "cmd" in expr:
            ctype = expr["cmd"]
            if ctype == "ttest":
                res = self._eval_ttest(expr)
                self.env[name] = res
                print(f"[Assigned t-test result to '{name}']")
            elif ctype == "regress":
                res = self._eval_regress(expr)
                self.env[name] = res
                print(f"[Assigned regression model to '{name}']")
            elif ctype == "load":
                fname = expr["file"]
                header = expr.get("header", False)
                df = pd.read_csv(fname, header=0 if header else 'infer')
                self.env[name] = df
                print(f"[Loaded '{fname}' into '{name}']")
            else:
                self.env[name] = expr
                print(f"[Assigned '{name}']")
        else:
            self.env[name] = self.env.get(expr) if isinstance(expr, str) else expr
            print(f"[Assigned '{name}']")

    def _cmd_ttest(self, cmd):
        res = self._eval_ttest(cmd)
        key = f"ttest_{len(self.env)}"
        self.env[key] = res
        print(f"[Stored t-test as '{key}']")
        return res

    def _eval_ttest(self, spec):
        target = spec["target"]
        ds_name = target["dataset"]
        col = target["column"]
        df = self.env.get(ds_name)
        if df is None:
            raise ValueError(f"Dataset '{ds_name}' not found")
        by = spec.get("by")
        against = spec.get("against")
        if by:
            series = df[[col, by]].dropna()
            groups = series[by].unique()
            if len(groups) != 2:
                raise ValueError("ttest by: found not exactly 2 groups")
            g1, g2 = groups
            s1 = series[series[by] == g1][col].dropna()
            s2 = series[series[by] == g2][col].dropna()
            res = stats.ttest_ind(s1, s2, equal_var=False)
            mean1, mean2 = s1.mean(), s2.mean()
            sd1, sd2 = s1.std(ddof=1), s2.std(ddof=1)
            n1, n2 = len(s1), len(s2)
            se = (sd1**2 / n1 + sd2**2 / n2) ** 0.5
            num = (sd1**2 / n1 + sd2**2 / n2) ** 2
            den = ((sd1**4)/(n1**2*(n1-1))) + ((sd2**4)/(n2**2*(n2-1)))
            dfw = num/den if den!=0 else n1+n2-2
            tcrit = stats.t.ppf(1-0.025, dfw)
            diff = mean1 - mean2
            ci_low, ci_high = diff - tcrit*se, diff + tcrit*se
            pooled_var = (((n1-1)*sd1**2)+((n2-1)*sd2**2))/(n1+n2-2)
            pooled_sd = pooled_var**0.5 if pooled_var>0 else np.nan
            cohens_d = (mean1-mean2)/pooled_sd if pooled_sd and pooled_sd>0 else np.nan
            return {"kind":"two-sample","group_names":(str(g1),str(g2)),
                    "mean1":float(mean1),"mean2":float(mean2),
                    "sd1":float(sd1),"sd2":float(sd2),
                    "n1":n1,"n2":n2,
                    "t":float(res.statistic),"p":float(res.pvalue),
                    "diff":float(diff),"ci":(ci_low,ci_high),"d":float(cohens_d)}
        else:
            mu = spec.get("against",0.0)
            series = df[col].dropna()
            if len(series)<2:
                raise ValueError("Not enough observations for t-test")
            res = stats.ttest_1samp(series,popmean=mu)
            mean = series.mean()
            sd = series.std(ddof=1)
            n = len(series)
            se = sd/(n**0.5)
            dfv = n-1
            tcrit = stats.t.ppf(1-0.025,dfv)
            diff = mean - mu
            ci_low, ci_high = diff - tcrit*se, diff + tcrit*se
            d = diff/sd if sd and sd>0 else np.nan
            return {"kind":"one-sample",
                    "mean":float(mean),
                    "sd":float(sd),
                    "n":n,
                    "t":float(res.statistic),
                    "p":float(res.pvalue),
                    "mu":float(mu),
                    "diff":float(diff),
                    "ci":(ci_low,ci_high),
                    "d":float(d)}

    def _cmd_regress(self, cmd):
        model = self._eval_regress(cmd)
        key = f"regress_{len(self.env)}"
        self.env[key] = model
        print(f"[Stored regression model as '{key}']")
        return model

    def _eval_regress(self, spec):
        dep = spec["dep"]
        predictors = spec["predictors"]
        dfname = spec["dataset"]
        df = self.env.get(dfname)
        if df is None:
            raise ValueError(f"Dataset '{dfname}' not found")
        # Convert Tree objects to strings if necessary
        predictors_str = []
        for t in predictors:
            if isinstance(t, str):
                predictors_str.append(t)
            elif hasattr(t, 'children') and t.data == 'term':
                predictors_str.append(str(t.children[0]))
            else:
                raise ValueError(f"Unknown predictor type: {t}")
        formula = dep + " ~ " + " + ".join(predictors_str)
        model = smf.ols(formula=formula, data=df).fit()
        return model


    def _cmd_plot(self, cmd):
        ds = self.env.get(cmd.get("dataset"))
        if ds is None:
            print("[plot] dataset not found:", cmd.get("dataset"))
            return
        x, y, kind_spec = cmd.get("x"), cmd.get("y"), cmd.get("kind")
        kind = kind_spec.get("kind") if kind_spec else None

        # Convert x/y if they are list (var.column)
        if isinstance(x,list):
            x_col = x[-1]
            ds_x = self.env.get(x[0]) if len(x)>1 else ds
        else:
            x_col, ds_x = x, ds

        y_col, ds_y = None, ds_x
        if y:
            if isinstance(y,list):
                y_col = y[-1]
                ds_y = self.env.get(y[0]) if len(y)>1 else ds
            else:
                y_col = y

        if kind=="histogram":
            bins = kind_spec.get("bins",20)
            ds_x[x_col].dropna().plot(kind="hist",bins=bins,title=f"Histogram of {x_col}")
        elif kind=="box":
            ds_x.boxplot(column=[x_col])
        elif kind == "scatter":
            if y_col:
                ds_x.plot(x=y_col, y=x_col, kind="scatter", title=f"{y_col} vs {x_col}")
            else:
                ds_x.plot(y=x_col, kind="scatter", title=f"{x_col}")
        plt.tight_layout()
        plt.show()

    def _cmd_conclude(self, cmd):
        name = cmd["name"]
        alpha = cmd.get("alpha", 0.05)
        obj = self.env.get(name)
        if obj is None:
            print("[conclude] unknown object:", name)
            return

        if isinstance(obj, dict):
            # t-test dict
            kind = obj.get("kind", "")
            if kind.startswith("one") or kind.startswith("two"):
                table_needed = generate_conclusion(obj, alpha=alpha, ask_table=self._ask_for_table)
                return
        else:
            # assume regression (statsmodels)
            model = obj
            print("\n=== Regression summary ===\n")
            print(model.summary())
            # generate text summary
            generate_conclusion(model, alpha=alpha, ask_table=self._ask_for_table)


    def _cmd_ask_table(self, cmd):
        key = cmd["key"]
        val = ask_user_for_table(key)
        self.user_tables[key] = val
        print(f"[Stored user table '{key}']")

    def _ask_for_table(self, key):
        if key in self.user_tables:
            return self.user_tables[key]
        val = ask_user_for_table(key)
        self.user_tables[key] = val
        return val
        
