class Expression:
    def __init__(self, content):
        """
        Класс для хранения любого логического выражения.
        content: объект класса Variable, Negation или Implication.
        """
        self.content = content

    def __repr__(self):
        return repr(self.content)

    def substitute(self, var, expr):
        """
        Заменяет все вхождения переменной var на выражение expr внутри content.
        """
        # Рекурсивно вызываем substitute у содержимого
        return Expression(self.content.substitute(var, expr))


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def substitute(self, var, expr):
        # Заменяет переменную, если она совпадает с подставляемой
        if self == var:
            return expr
        return self


class Negation:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"¬{self.expression}"

    def __eq__(self, other):
        return isinstance(other, Negation) and self.expression == other.expression

    def substitute(self, var, expr):
        # Заменяем переменную внутри отрицания
        return Negation(self.expression.substitute(var, expr))


class Implication:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"({self.antecedent} → {self.consequent})"

    def __eq__(self, other):
        return (isinstance(other, Implication) and
                self.antecedent == other.antecedent and
                self.consequent == other.consequent)

    def substitute(self, var, expr):
        # Заменяем переменную в обеих частях импликации
        new_antecedent = self.antecedent.substitute(var, expr)
        new_consequent = self.consequent.substitute(var, expr)
        return Implication(new_antecedent, new_consequent)


A = Variable("A")
B = Variable("B")
C = Variable("C")

# Создаем выражения с использованием переменных, отрицаний и импликаций
expr1 = Expression(Implication(A, Negation(B)))  # (A → ¬B)
expr2 = Expression(Implication(expr1, C))  # ((A → ¬B) → C)

axiom1 = Implication(A, Implication(B, A))  # A1: (A → (B → A))
axiom2 = Implication(Implication(A, Implication(B, C)), Implication(Implication(A, B), Implication(A, C)))  # A2
axiom3 = Implication(Implication(Negation(B), Negation(A)), Implication(Implication(Negation(B), A), B))  # A3

print("Исходное выражение:", axiom2)

# Подстановка: заменим A на (B → C)
new_expr = axiom2.substitute('A', axiom1)

print("После замены A на (B → C):", new_expr)
