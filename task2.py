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

    # Правила вывода
    def modus_ponens(self, expr1, expr2):
        if isinstance(expr1, Implication) and expr1.antecedent == expr2:
            return expr1.consequent
        return None

    def modus_tollens(self, expr1, expr2):
        if isinstance(expr1, Implication) and isinstance(expr2, Negation):
            if expr1.consequent == expr2.expression:
                return Negation(expr1.antecedent)
        return None

    def disjunctive_syllogism(self, expr1, expr2):
        if isinstance(expr1, Negation) and isinstance(expr2, Implication):
            if expr2.antecedent == expr1.expression:
                return expr2.consequent
        return None

    def hypothetical_syllogism(self, expr1, expr2):
        if isinstance(expr1, Implication) and isinstance(expr2, Implication):
            if expr1.consequent == expr2.antecedent:
                return Implication(expr1.antecedent, expr2.consequent)
        return None

    def complex_constructive_dilemma(self, expr1, expr2, expr3):
        if (isinstance(expr1, Implication) and isinstance(expr2, Implication) and
                isinstance(expr3, Implication) and isinstance(expr3.antecedent, Variable)):
            if expr1.antecedent == expr3.antecedent and expr2.antecedent == expr3.consequent:
                return Implication(expr1.consequent, expr2.consequent)
        return None


    def step(self):
        new_expressions = set()
        # Применяем каждый из правил к парам теорем
        for expr1 in self.identities:
            for expr2 in self.identities:
                new_expr = (
                        self.modus_ponens(expr1, expr2) or
                        self.modus_tollens(expr1, expr2) or
                        self.disjunctive_syllogism(expr1, expr2) or
                        self.hypothetical_syllogism(expr1, expr2)
                )
                if new_expr and new_expr not in self.identities:
                    new_expressions.add(new_expr)

        # Добавляем новые выражения в доказанные
        self.identities.extend(new_expressions)


    def print_all_identities(self):
        for i in self.identities:
            print(repr(i))

    # Основной метод доказательства
    def proof(self, target):
        while target not in self.identities:
            self.step()
            if target in self.identities:
                print(f"Доказано: {target}")
                return True
            else:
                print(f"Не удалось доказать: {target}")
                return False
        print(f"Доказано: {target}")
        return True


prover = AutoProof()

# Пример доказательства
A = Variable("A")
B = Variable("B")
target = Implication(A, B)
prover.proof(target)
