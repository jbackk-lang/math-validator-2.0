# filters/misleading_filter.py

import re

def run(p):
    """
    Filtr MISLEADING — wykrywa problemy mylne:
    - wielokrotne '='
    - łańcuchowe porównania
    - niejednoznaczne konstrukcje
    - 0^0
    - x/x bez kontekstu
    """

    expr = p.raw.replace(" ", "")

    # 1. Wielokrotne '='
    if expr.count("=") > 1:
        return {"misleading": True, "reason": "multiple_equal_signs"}

    # 2. a=b=c
    if re.search(r"[a-zA-Z]+\=[a-zA-Z]+\=[a-zA-Z]+", expr):
        return {"misleading": True, "reason": "chained_comparison"}

    # 3. (a=b=c)
    if re.search(r"\([^\)]*\=[^\)]*\=[^\)]*\)", expr):
        return {"misleading": True, "reason": "chained_comparison_parentheses"}

    # 4. 0^0
    if "0^0" in expr:
        return {"misleading": True, "reason": "zero_power_zero"}

    # 5. x/x (może być 0/0)
    if re.fullmatch(r"[a-zA-Z]+/[a-zA-Z]+", expr):
        return {"misleading": True, "reason": "ambiguous_division"}

    return {"misleading": False}
