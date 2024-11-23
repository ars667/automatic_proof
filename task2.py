class Expression:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return repr(self.content)

    def __eq__(self, other):
        return isinstance(other, Expression) and self.content == other.content

    def substitute(self, var, expr):
        return Expression(self.content.substitute(var, expr))


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def substitute(self, var, expr):
        return expr if self == var else self


class Negation:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"¬{self.expression}"

    def __eq__(self, other):
        return isinstance(other, Negation) and self.expression == other.expression

    def substitute(self, var, expr):
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
        new_antecedent = self.antecedent.substitute(var, expr)
        new_consequent = self.consequent.substitute(var, expr)
        return Implication(new_antecedent, new_consequent)


class AutoProof:
    def __init__(self):
        A = Variable("A")
        B = Variable("B")
        C = Variable("C")

        # Аксиомы
        A1 = Implication(A, Implication(B, A))
        A2 = Implication(Implication(A, Implication(B, C)), Implication(Implication(A, B), Implication(A, C)))
        A3 = Implication(Implication(Negation(B), Negation(A)), Implication(Implication(Negation(B), A), B))

        # Основные тождества
        self.identities = [A1, A2, A3]
        self.variables = [A, B, C]

    # Правила вывода:
    # Модус поненс
    def modus_ponsens(self, expr1, expr2):
        new_expressions = []
        if isinstance(expr1, Implication):
            if isinstance(expr1.antecedent, Variable):
                new_expressions.append(expr1.consequent.substitute(expr1.antecedent, expr2))
            if isinstance(expr1.antecedent, Implication):
                for ant in self.modus_ponsens(expr1.antecedent, expr2):
                    new_expressions.append(Implication(ant, expr1.consequent))
        if isinstance(expr1, Negation):
            for neg in self.modus_ponsens(expr1.expression, expr2):
                new_expressions.append(Negation(neg))
        return new_expressions

    # Модус толленс
    def modus_tollens(self, expr1, expr2):
        new_expressions = []
        if isinstance(expr1, Implication) and isinstance(expr2, Negation):
            if expr1.consequent == expr2.expression:
                 new_expressions.append(Negation(expr1.antecedent)) #
        elif isinstance(expr1, Implication):
            antecedent_results = self.modus_tollens(expr1.antecedent, expr2)#
            consequent_results = self.modus_tollens(expr1.consequent, expr2)#
            for ant in antecedent_results:#
                new_expressions.append(Implication(ant, expr1.consequent))#
            for cons in consequent_results:
                new_expressions.append(Implication(expr1.antecedent, cons))#
        elif isinstance(expr1, Negation):#
            negated_results = self.modus_tollens(expr1.expression, expr2)#
            for neg in negated_results:#
                new_expressions.append(Negation(neg))#
        return new_expressions#

    # Разделительный силлогизм
    def disjunctive_syllogism(self, expr1, expr2):
        if isinstance(expr1, Negation):
            deeper = self.disjunctive_syllogism(expr1.expression, expr2)
            if deeper:
                return Negation(deeper)

        if isinstance(expr2, Implication):
            new_antecedent = self.disjunctive_syllogism(expr1, expr2.antecedent)
            new_consequent = self.disjunctive_syllogism(expr1, expr2.consequent)
            return Implication(new_antecedent or expr2.antecedent, new_consequent or expr2.consequent)

        return None
    
        def hypothetical_syllogism(self, expr1, expr2):
        if isinstance(expr1, Implication):
            new_antecedent = self.hypothetical_syllogism(expr1.antecedent, expr2)
            new_consequent = self.hypothetical_syllogism(expr1.consequent, expr2)

            return Implication(new_antecedent or expr1.antecedent, new_consequent or expr1.consequent)
        if isinstance(expr2, Implication):
            new_antecedent = self.hypothetical_syllogism(expr1, expr2.antecedent)
            new_consequent = self.hypothetical_syllogism(expr1, expr2.consequent)

            return Implication(new_antecedent or expr2.antecedent, new_consequent or expr2.consequent)
        elif isinstance(expr1, Negation):

            negated_expr = self.hypothetical_syllogism(expr1.expression, expr2)
            if negated_expr:
                return Negation(negated_expr)
        return None

    # Простая конструктивная дилемма
    def simple_constructive_dilemma(self, expr1, expr2):
        if isinstance(expr1, Implication) and isinstance(expr2, Implication):
            if expr1.antecedent == expr2.antecedent:
                return Implication(expr1.consequent, expr2.consequent)
        elif isinstance(expr1, Negation):

            negated_expr = self.simple_constructive_dilemma(expr1.expression, expr2)
            if negated_expr:
                return Negation(negated_expr)

        return None

    # Сложная конструктивная дилемма
    def complex_constructive_dilemma(self, expr1, expr2, expr3):
        if isinstance(expr1, Implication) and isinstance(expr2, Implication) and isinstance(expr3, Implication):
            if expr1.antecedent == expr3.antecedent and expr2.antecedent == expr3.consequent:
                return Implication(expr1.consequent, expr2.consequent)
        elif isinstance(expr1, Negation):

            negated_expr = self.complex_constructive_dilemma(expr1.expression, expr2, expr3)
            if negated_expr:
                return Negation(negated_expr)

        return None

    def simple_destructive_dilemma(self, impl1, impl2, disjunction):
        new_expressions = []
        if (isinstance(impl1, Implication) and isinstance(impl2, Implication)
                and impl1.antecedent == impl2.antecedent
                and isinstance(disjunction, Implication)):
            if disjunction.consequent == Negation(impl1.consequent) or disjunction.antecedent == Negation(impl2.consequent):
                new_expressions.append(Negation(impl1.antecedent))
        return new_expressions

    def complex_destructive_dilemma(self, impl1, impl2, disjunction):
        new_expressions = []
        if (isinstance(impl1, Implication) and isinstance(impl2, Implication)
                and isinstance(disjunction, Implication)):
            if (disjunction.antecedent == Negation(impl1.consequent)
                    and disjunction.consequent == Negation(impl2.consequent)):
                new_expressions.append(Implication(Negation(impl1.antecedent), Negation(impl2.antecedent)))
        return new_expressions

    def is_uniq(self, expr, arr):
        return all((not (i.__eq__(expr))) for i in arr)

    def step(self):
        new_exprssions = []
        for i in self.identities:
            for j in self.identities:
                new = self.modus_tollens(i,j)
                for x in new:
                    if self.is_uniq(x, self.identities) and self.is_uniq(x, new_exprssions):
                        new_exprssions.append(x)
        self.make_new_identities()
        for i in new_exprssions:
            self.identities.append(i)

    def make_new_identities(self):
        old = self.identities.copy()
        for identity in old:
            A_B_identity = identity.substitute(Variable('A'), Variable('X'))
            A_B_identity = A_B_identity.substitute(Variable('B'), Variable('A'))
            A_B_identity = A_B_identity.substitute(Variable('X'), Variable('B'))
            self.identities.append(A_B_identity)

            A_A_identity = identity.substitute(Variable('B'), Variable('A'))
            self.identities.append(A_A_identity)

    def print_all_identities(self):
        for i in self.identities:
            print(repr(i))

    def proof(self, target):
        while True:
            self.step()
            for i in target:
                for j in self.identities:
                    if i.__eq__(j):
                        print("proofed!:", j)
                        return False



proofer = Auto_proof()

A = Variable("A")
B = Variable("B")
C = Variable("C")

target = [

    Implication(Negation(Implication(A, Negation(B))), A),
]

proofer.proof(target)
