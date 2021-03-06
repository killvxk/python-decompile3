from decompyle3 import code_deparse

from io import StringIO

out = StringIO()

def run_deparse(expr: str, compile_mode: bool, debug=False) -> object:
    if debug:
        debug_opts = {"asm": "both", "tree": True, "grammar": True}
    else:
        debug_opts = {"asm": False, "tree": False, "grammar": False}

    if compile_mode == "lambda":
        compile_mode = "eval"
    code = compile(expr + "\n", "<string %s>" % expr, compile_mode)
    deparsed = code_deparse(code, out=out, compile_mode=compile_mode, debug_opts=debug_opts)
    return deparsed


# FIXME: DRY this code
def test_single_mode() -> None:
    expressions = (
        "1",
        "I and (j or k)",
        "j % 4",
        "i = 1",
        "i += 1",
        "i = j % 4",
        "i = {}",
        "i = []",
        "for i in range(10):\n    i\n",
        "for i in range(10):\n    for j in range(10):\n        i + j\n",
        # "try:\n    i\nexcept Exception:\n    j\nelse:\n    k\n"
    )

    for expr in expressions:
        deparsed = run_deparse(expr, compile_mode="single")
        assert deparsed.text == expr + "\n"

def test_eval_mode():
    expressions = (
        "1",
        "j % 4",
        "i and (j or k)",
    )

    for expr in expressions:
        deparsed = run_deparse(expr, compile_mode="eval")
        # print(expr, "vs.", deparsed.text)
        assert deparsed.text == expr

def test_lambda_mode():
    expressions = (
        "lambda d=b'': 5",
        "lambda *, d=0: d",
        "lambda x: 1 if x < 2 else 3",
        "lambda y: x * y",
    )

    for expr in expressions:
        deparsed = run_deparse(expr, compile_mode="lambda")
        # print(expr, "vs.", deparsed.text)
        assert deparsed.text == expr

if __name__ == "__main__":
    test_eval_mode()
    test_lambda_mode()
    test_single_mode()
