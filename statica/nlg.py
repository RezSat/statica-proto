import math
import textwrap

def ask_user_for_table(key: str):
    """
    Prompt the user for a table value or accept input.
    Example: key = "t_critical", user may enter numeric 2.447.
    Return float or structured input as needed.
    """
    print(f"\nStatica requests a value from a statistical table: '{key}'.")
    print("Provide the numeric value (or type 'auto' to let Statica compute an approximation):")
    while True:
        user = input(f"Enter value for '{key}': ").strip()
        if user.lower() == "auto":
            print("[User selected auto — Statica will approximate if possible.]")
            return "auto"
        try:
            val = float(user)
            return val
        except ValueError:
            print("Please enter a number or 'auto'.")

def _format_p(p):
    if p < 0.001:
        return "<0.001"
    return f"{p:.3f}"

def generate_conclusion(result, alpha=0.05, ask_table=None):
    """
    Template-based NLG:
    - If result is a t-test dict, we produce a human-like paragraph.
    - If result is a statsmodels RegressionResultsWrapper, produce a short summary.
    The ask_table callback is optional; when a precise table lookup is required,
    we call ask_table(key) to retrieve user-provided values.
    """
    # Two-sample
    if isinstance(result, dict) and result.get("kind") == "two-sample":
        g1, g2 = result["group_names"]
        mean1, mean2 = result["mean1"], result["mean2"]
        diff = result["diff"]
        ci_low, ci_high = result["ci"]
        t, p = result["t"], result["p"]
        d = result.get("d", float("nan"))
        ptxt = _format_p(p)
        sig = p < alpha
        mag = "unknown"
        if not math.isnan(d):
            ad = abs(d)
            if ad < 0.2:
                mag = "negligible"
            elif ad < 0.5:
                mag = "small"
            elif ad < 0.8:
                mag = "medium"
            else:
                mag = "large"

        lines = []
        lines.append(f"A two-sample comparison between group '{g1}' (mean={mean1:.2f}) and '{g2}' (mean={mean2:.2f}) was conducted.")
        lines.append(f"Mean difference = {diff:.2f} (95% CI [{ci_low:.2f}, {ci_high:.2f}]). Test statistic t = {t:.2f}, p = {ptxt}.")
        if sig:
            lines.append(f"This result is statistically significant at alpha={alpha}.")
        else:
            lines.append(f"No statistically significant difference observed at alpha={alpha}.")
        lines.append(f"Effect size (Cohen's d) = {d:.2f} ({mag} effect).")
        # Practical interpretation
        direction = "higher" if mean1 > mean2 else "lower"
        lines.append(f"Practical interpretation: on average, observations in group '{g1}' are {direction} than in '{g2}'.")
        out = "\n".join(lines)
        print("\n=== Conclusion (Statica) ===\n")
        print(textwrap.fill(out, width=100))
        print("\n============================\n")
        return None

    # One-sample
    if isinstance(result, dict) and result.get("kind") == "one-sample":
        mean = result["mean"]
        mu = result["mu"]
        diff = result["diff"]
        ci_low, ci_high = result["ci"]
        t, p = result["t"], result["p"]
        d = result.get("d", float("nan"))
        ptxt = _format_p(p)
        sig = p < alpha
        lines = []
        lines.append(f"A one-sample t-test compared the sample mean ({mean:.2f}, n={result['n']}) to {mu}.")
        lines.append(f"Mean difference = {diff:.2f} (95% CI [{ci_low:.2f}, {ci_high:.2f}]). t = {t:.2f}, p = {ptxt}.")
        if sig:
            lines.append(f"Conclusion: the sample mean differs from {mu} at alpha={alpha}.")
        else:
            lines.append(f"Conclusion: no evidence that the sample mean differs from {mu} at alpha={alpha}.")
        if not math.isnan(d):
            lines.append(f"Cohen's d = {d:.2f}.")
        print("\n=== Conclusion (Statica) ===\n")
        print(textwrap.fill("\n".join(lines), width=100))
        print("\n============================\n")
        return None

    # Regression (statsmodels)
    try:
        # For statsmodels RegressionResultsWrapper
        from statsmodels.regression.linear_model import RegressionResultsWrapper
        if isinstance(result, RegressionResultsWrapper):
            rs = result
            coef = rs.params
            pvals = rs.pvalues
            r2 = rs.rsquared
            lines = []
            lines.append(f"Linear regression (OLS) summary: R² = {r2:.3f}.")
            # report top predictors (non-const)
            for var in coef.index:
                if var == "Intercept":
                    continue
                lines.append(f"Predictor '{var}': β = {coef[var]:.3f}, p = {_format_p(pvals[var])}.")
            # give high-level interpretation
            lines.append("Interpretation: predictors with p < 0.05 are considered statistically associated with the outcome.")
            print("\n=== Conclusion (Statica - Regression) ===\n")
            print("\n".join(lines))
            print("\n============================\n")
            return None
    except Exception:
        pass

    print("[NLG] Unrecognized result type for conclusion.")
    return None
