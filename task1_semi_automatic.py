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
        return (isinstance(other,
                           Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent)

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
        axiom3 = Implication(Implication(A, Implication(B, A)), Implication(A, A))
        self.identities = [axiom1, axiom2, axiom3]
        #self.identities = [axiom1, axiom2]

    def modus_ponsens(self, expr1, expr2):
        new_expressions = []
        if isinstance(expr1, Implication):
            if expr1.antecedent.__eq__(expr2):
                new_expressions.append(expr1.consequent)
            if isinstance(expr1.antecedent, Variable):
                new_expressions.append(expr1.consequent.substitute(expr1.antecedent, expr2))
            if isinstance(expr1.antecedent, Implication):
                for ant in self.modus_ponsens(expr1.antecedent, expr2):
                    new_expressions.append(Implication(ant, expr1.consequent))
        if isinstance(expr1, Negation):
            for neg in self.modus_ponsens(expr1.expression, expr2):
                new_expressions.append(Negation(neg))
        return new_expressions

    def is_uniq(self, expr, arr):
        return all((not (i.__eq__(expr))) for i in arr)

    def step(self):
        new_exprssions = []
        for i in self.identities:
            for j in self.identities:
                new = self.modus_ponsens(i, j)
                for x in new:
                    if self.is_uniq(x, self.identities) and self.is_uniq(x, new_exprssions):
                        new_exprssions.append(x)
        self.make_new_identities()
        for i in new_exprssions:
            self.identities.append(i)

    def make_new_identities(self):
        old = self.identities.copy()
        for identity in old:
            A_B_C_identity = identity.substitute(Variable('C'), Variable('A'))
            self.identities.append(A_B_C_identity)

            A_B_identity = identity.substitute(Variable('A'), Variable('X'))
            A_B_identity = A_B_identity.substitute(Variable('B'), Variable('A'))
            A_B_identity = A_B_identity.substitute(Variable('X'), Variable('B'))
            self.identities.append(A_B_identity)

            A_A_identity = identity.substitute(Variable('B'), Variable('A'))
            self.identities.append(A_A_identity)

            B_BA_identity = identity.substitute(Variable('B'), Implication(Variable('B'), Variable('A')))
            A_AB_identity = identity.substitute(Variable('A'), Implication(Variable('A'), Variable('B')))
            self.identities.append((B_BA_identity))
            self.identities.append((A_AB_identity))

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
    #Implication(Implication(A, B), Implication(A, A)),
    Implication(Implication(A, Implication(B, A)), Implication(A, A)),
    Implication(A, A),
    Implication(Negation(Implication(A, Negation(B))), A),
    Implication(Negation(Implication(A, Negation(B))), B),
    Implication(A, Implication(B, Negation(Implication(A, Negation(B))))),
    Implication(A, Implication(Negation(A), B)),
    Implication(B, Implication(Negation(A), B)),
    Implication(Negation(A), Implication(A, B)),
    Implication(Negation(A), Negation(A)),
    # Implication(Implication(A, B), Implication(A, (Implication(C, Implication(Implication(A, B), Implication(A, C))))))
]

proofer.proof(target)
