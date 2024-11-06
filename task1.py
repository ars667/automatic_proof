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


class Auto_proof:
    def __init__(self):
        A = Variable("A")
        B = Variable("B")
        C = Variable("C")
        axiom1 = Implication(A, Implication(B, A))
        axiom2 = Implication(Implication(A, Implication(B, C)), Implication(Implication(A, B), Implication(A, C)))
        axiom3 = Implication(Implication(Negation(B), Negation(A)), Implication(Implication(Negation(B), A), B))
        self.identities = [axiom1, axiom2, axiom3]

    def step(self):
        new_exprssions = []
        for i in self.identities:
            for j in self.identities:
                if isinstance(i, Implication):
                    if isinstance(i.antecedent, Variable):
                        new_exprssions.append(i.consequent.substitute(i.antecedent, j))
        for i in new_exprssions:
            self.identities.append(i)

    def print_all_identities(self):
        for i in self.identities:
            print(repr(i))


proofer = Auto_proof()
proofer.step()
proofer.step()
proofer.print_all_identities()
