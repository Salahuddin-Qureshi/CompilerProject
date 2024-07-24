import tkinter as tk

# Token types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULTIPLY = 'MULTIPLY'
DIVIDE = 'DIVIDE'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

# Lexer
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                token = Token(INTEGER, self.integer())
                print("Token:", token)
                return token
            if self.current_char == '+':
                self.advance()
                token = Token(PLUS, '+')
                print("Token:", token)
                return token
            if self.current_char == '-':
                self.advance()
                token = Token(MINUS, '-')
                print("Token:", token)
                return token
            if self.current_char == '*':
                self.advance()
                token = Token(MULTIPLY, '*')
                print("Token:", token)
                return token
            if self.current_char == '/':
                self.advance()
                token = Token(DIVIDE, '/')
                print("Token:", token)
                return token
            if self.current_char == '(':
                self.advance()
                token = Token(LPAREN, '(')
                print("Token:", token)
                return token
            if self.current_char == ')':
                self.advance()
                token = Token(RPAREN, ')')
                print("Token:", token)
                return token
            self.error()
        return Token(EOF, None)

# Parser
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token.value)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type in (MULTIPLY, DIVIDE):
            token = self.current_token
            if token.type == MULTIPLY:
                self.eat(MULTIPLY)
            elif token.type == DIVIDE:
                self.eat(DIVIDE)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

# Syntax Tree nodes
# Syntax Tree nodes
class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return self._str_helper(0)

    def _str_helper(self, indentation):
        op_str = str(self.op.value)
        left_str = self.left._str_helper(indentation + 4) if isinstance(self.left, BinOp) else str(self.left)
        right_str = self.right._str_helper(indentation + 4) if isinstance(self.right, BinOp) else str(self.right)
        return f"{' ' * indentation}{op_str}\n{' ' * (indentation + len(op_str))}/{' ' * (indentation + 1)}\\\n{left_str}{' ' * (indentation + len(op_str))}{right_str}"


class Num:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Evaluation
def visit(node):
    if isinstance(node, Num):
        return node.value
    elif isinstance(node, BinOp):
        if node.op.type == PLUS:
            return visit(node.left) + visit(node.right)
        elif node.op.type == MINUS:
            return visit(node.left) - visit(node.right)
        elif node.op.type == MULTIPLY:
            return visit(node.left) * visit(node.right)
        elif node.op.type == DIVIDE:
            right_value = visit(node.right)
            if right_value == 0:
                raise ZeroDivisionError("Division by zero")
            return visit(node.left) / right_value


def evaluate(expression):
    lexer = Lexer(expression)
    parser = Parser(lexer)
    tree = parser.expr()
    result = visit(tree)
    return tree, result

def display_tree_and_result(expression):
    try:
        tree, result = evaluate(expression)

        root = tk.Tk()
        root.title("Syntax Tree and Result")

        tree_text = str(tree)
        tree_label = tk.Label(root, text=tree_text, font=("Courier", 12), justify="left")
        tree_label.pack(padx=20, pady=10)

        result_label = tk.Label(root, text=f"Result: {result}", font=("Courier", 12))
        result_label.pack(padx=20, pady=10)

        root.mainloop()
    except ZeroDivisionError as e:
        print("Error:", e)


# Test
if __name__ == '__main__':
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        display_tree_and_result(text)
