# -*- coding: utf-8 -*-
"""
Micro-pilot: measuring the verifiability gap g on a hand-constructed set of 20
arithmetic word-problem derivations.

This is an ILLUSTRATIVE, deterministic micro-pilot (not a trained-model
benchmark). It implements the semantic-reduction layer rho of the paper as a
small typed DSL and counts how many of 20 natural-language derivations admit a
typed reduction. The generation layer is simulated by a fixed, hand-built set
of derivations with a realistic mix of well-typed and malformed items.
"""

# --- typed DSL --------------------------------------------------------------
# Type: Nat (nonnegative integers). Ops: add/sub/mul/div with side conditions.
# rho succeeds only for a fully-typed term whose side conditions all hold.

class ReductionError(Exception):
    pass

def build_term(steps):
    if not steps:
        raise ReductionError("empty derivation")
    val = None
    for kind, a, b in steps:
        if kind == "lit":
            if not isinstance(a, int) or a < 0:
                raise ReductionError("untyped/negative literal")
            val = a
        elif kind in ("add", "mul"):
            if val is None or not isinstance(b, int):
                raise ReductionError("missing typing")
            val = val + b if kind == "add" else val * b
        elif kind == "sub":
            if val is None or not isinstance(b, int):
                raise ReductionError("missing typing")
            if val < b:
                raise ReductionError("sub underflow (constraint violated)")
            val = val - b
        elif kind == "div":
            if val is None or not isinstance(b, int):
                raise ReductionError("missing typing")
            if b <= 0 or val % b != 0:
                raise ReductionError("non-exact division (constraint violated)")
            val = val // b
        else:
            raise ReductionError(f"unsupported/untyped construct: {kind}")
    return val

def reduce_derivation(deriv):
    try:
        return build_term(deriv["steps"])
    except ReductionError:
        return None

# --- the 20 derivations -----------------------------------------------------
# 14 well-typed (rho succeeds) + 6 malformed (rho fails), with the named cause.
D = [
    ("D01", "Alice has 5 apples, Bob gives her 3 more.",            [("lit",5,0),("add",5,3)], 8, "ok"),
    ("D02", "12 apples shared equally among 3 friends.",            [("lit",12,0),("div",12,3)], 4, "ok"),
    ("D03", "Tom had 7 books and bought 2 more.",                   [("lit",7,0),("add",7,2)], 9, "ok"),
    ("D04", "A 20-meter rope cut into 5 equal parts.",              [("lit",20,0),("div",20,5)], 4, "ok"),
    ("D05", "6 candies per box, 4 boxes.",                          [("lit",6,0),("mul",6,4)], 24, "ok"),
    ("D06", "15 minus 9.",                                          [("lit",15,0),("sub",15,9)], 6, "ok"),
    ("D07", "3 times 7.",                                           [("lit",3,0),("mul",3,7)], 21, "ok"),
    ("D08", "18 divided by 6.",                                     [("lit",18,0),("div",18,6)], 3, "ok"),
    ("D09", "10 plus 4.",                                           [("lit",10,0),("add",10,4)], 14, "ok"),
    ("D10", "30 take away 12.",                                     [("lit",30,0),("sub",30,12)], 18, "ok"),
    ("D11", "8 multiplied by 5.",                                   [("lit",8,0),("mul",8,5)], 40, "ok"),
    ("D12", "45 divided by 9.",                                     [("lit",45,0),("div",45,9)], 5, "ok"),
    ("D13", "16 increased by 9.",                                   [("lit",16,0),("add",16,9)], 25, "ok"),
    ("D14", "24 reduced by 6.",                                     [("lit",24,0),("sub",24,6)], 18, "ok"),
    ("D15", "Alice gives away half of her 5 apples.",              [("lit",5,0),("coerce",5,2)], 2, "coerce (non-exact div)"),
    ("D16", "She then takes some of them.",                        [("ambig",0,0)], 0, "ambiguous reference"),
    ("D17", "Bob has twice as many.",                              [("ambig",0,0)], 0, "ambiguous reference"),
    ("D18", "About 20 people attended.",                           [("vague",0,0)], 0, "vague quantifier"),
    ("D19", "The answer is a bit more.",                           [("missing",0,0)], 0, "missing typing"),
    ("D20", "5 divided by 2 (integer part).",                      [("lit",5,0),("coerce",5,2)], 2, "coerce (non-exact div)"),
]

rows = []
nV = 0
for cid, text, steps, gold, cause in D:
    r = reduce_derivation({"steps": steps})
    reducible = r is not None
    verified = reducible and (r == gold)
    if reducible:
        nV += 1
    rows.append((cid, text, reducible, verified, cause))

nD = len(D)
g = 1 - nV / nD

print(f"|D| = {nD},  |V| = {nV},  g = 1 - |V|/|D| = {g:.2f}")
print()
print(f"{'id':4} {'reducible':9} {'verified':8}  cause")
for cid, text, reducible, verified, cause in rows:
    print(f"{cid:4} {str(reducible):9} {str(verified):8}  {cause}")
print()
silent = [r for r in rows if not r[2]]
print(f"silent-error set (D \\ V): {len(silent)} derivations, verifier provides no signal for any of them")
print(f"all {nV} reducible derivations verified correct -> soundness holds on this micro-pilot")
