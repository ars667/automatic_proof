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
        return (isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent)

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

    def modus_ponsens(self, expr1, expr2):
        if isinstance(expr1, Implication):
            if isinstance(expr1.antecedent, Variable):
                return expr1.consequent.substitute(expr1.antecedent, expr2)
            if isinstance(expr1.antecedent, Implication):
                return Implication(self.modus_ponsens(expr1.antecedent, expr2), expr1.consequent)
            if isinstance(expr1, Negation):
                return Negation(self.modus_ponsens(expr1.expression, expr2))
            if isinstance(expr1, Variable):
                return expr1
        return expr1

    def is_uniq(self, expr, arr):
        return all((not (i.__eq__(expr))) for i in arr)

    def step(self):
        new_exprssions = []
        for i in self.identities:
            for j in self.identities:
                new = self.modus_ponsens(i, j)
                if self.is_uniq(new, self.identities) and self.is_uniq(new, new_exprssions):
                    new_exprssions.append(new)
        for i in new_exprssions:
            self.identities.append(i)

    def print_all_identities(self):
        for i in self.identities:
            print(repr(i))

    def proof(self, target):
        while True:
            self.print_all_identities()
            self.step()
            for i in target:
                for j in self.identities:
                    if i.__eq__(j):
                        print("proofed!")


proofer = Auto_proof()

A = Variable("A")
B = Variable("B")
C = Variable("C")

target = [
    Implication(Negation(Implication(A, B)), A),
    Implication(Implication(A, B), B),
    Implication(A, Implication(B, Implication(A, B))),
    Implication(A, Implication(A, B)),
    Implication(B, Implication(A, B)),
    Implication(Implication(A, C), Implication(Implication(B, C), Implication(Implication(A, B), C))),
    Implication(Negation(A), Implication(A, B)),
    Implication(A, Negation(A))
]

proofer.proof(target)
