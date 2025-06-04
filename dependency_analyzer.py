import ast

class DependencyAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.function_defs = {}  # name -> full source
        self.function_calls = {}  # line number -> set of function names
        self.current_function = None

    def visit_FunctionDef(self, node):
        name = node.name
        start_lineno = node.lineno
        end_lineno = max([n.lineno for n in ast.walk(node) if hasattr(n, 'lineno')])
        self.function_defs[name] = (start_lineno, end_lineno)
        self.current_function = name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if hasattr(node.func, 'id'):
            if self.current_function:
                self.function_calls.setdefault(self.current_function, set()).add(node.func.id)
        self.generic_visit(node)

def get_dependencies(code: str):
    """
    Returns:
    - function_defs: {func_name: (start_line, end_line)}
    - call_map: {caller_func_name: set(called_func_names)}
    """
    tree = ast.parse(code)
    analyzer = DependencyAnalyzer()
    analyzer.visit(tree)
    return analyzer.function_defs, analyzer.function_calls
