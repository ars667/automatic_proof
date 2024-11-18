class Expression:
    def __init__(self, content):
        self.content = content

    def __repr__(self):
        return repr(self.content)

    def substitute(self, var, expr):
        return Expression(self.content.substitute(var, expr))

    def simplify(self):
        return Expression(self.content.simplify())


class Variable:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def substitute(self, var, expr):
        if self == var:
            return expr
        return self

    def simplify(self):
        return self  # Переменная остаётся без изменений


class Negation:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"¬{self.expression}"

    def __eq__(self, other):
        return isinstance(other, Negation) and self.expression == other.expression

    def __hash__(self):
        return hash(self.expression)

    def substitute(self, var, expr):
        return Negation(self.expression.substitute(var, expr))

    def simplify(self):
        return Negation(self.expression.simplify())


class Implication:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    def __repr__(self):
        return f"({self.antecedent} → {self.consequent})"

    def __eq__(self, other):
        return isinstance(other, Implication) and self.antecedent == other.antecedent and self.consequent == other.consequent

    def __hash__(self):
        return hash((self.antecedent, self.consequent))

    def substitute(self, var, expr):
        new_antecedent = self.antecedent.substitute(var, expr)
        new_consequent = self.consequent.substitute(var, expr)
        return Implication(new_antecedent, new_consequent)

    def simplify(self):
        # A → B эквивалентно ¬A ∨ B
        return Disjunction(Negation(self.antecedent), self.consequent)


class Disjunction:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.left} ∨ {self.right})"

    def __eq__(self, other):
        return isinstance(other, Disjunction) and self.left == other.left and self.right == other.right

    def __hash__(self):
        return hash((self.left, self.right))

    def substitute(self, var, expr):
        new_left = self.left.substitute(var, expr)
        new_right = self.right.substitute(var, expr)
        return Disjunction(new_left, new_right)

    def simplify(self):
        return Disjunction(self.left.simplify(), self.right.simplify())


def extract_literals(expression):
    """
    Извлекает все литералы (переменные и их отрицания) из выражения.
    """
    if isinstance(expression, Variable) or isinstance(expression, Negation):
        return [expression]
    elif isinstance(expression, Disjunction):
        return extract_literals(expression.left) + extract_literals(expression.right)
    else:
        return []



def resolve(clause1, clause2):
    """
    Применяет правило резолюции к двум дизъюнктам.
    Возвращает новый дизъюнкт или None, если резолюция невозможна.
    """
    literals1 = set(extract_literals(clause1))  # Преобразуем в множество
    literals2 = set(extract_literals(clause2))  # Преобразуем в множество
    resolvent_found = False
    new_literals = set()

    for lit1 in literals1:
        for lit2 in literals2:
            if isinstance(lit1, Negation) and lit1.expression == lit2:
                # Найдено противоположное утверждение
                resolvent_found = True
                new_literals = (literals1 - {lit1}) | (literals2 - {lit2})
            elif isinstance(lit2, Negation) and lit2.expression == lit1:
                # Найдено противоположное утверждение
                resolvent_found = True
                new_literals = (literals1 - {lit1}) | (literals2 - {lit2})

    if not resolvent_found:
        return None

    # Формируем новый дизъюнкт
    if not new_literals:  # Если пустой набор литералов, это противоречие
        return Expression(Variable("⊥"))

    new_clause = None
    for lit in new_literals:
        new_clause = Disjunction(new_clause, lit) if new_clause else lit

    return new_clause




def check_consistency(clauses):
    """
    Проверяет противоречивость множества посылок с использованием метода резолюции.
    """
    simplified_clauses = {clause.simplify().content for clause in clauses}

    print("Начальные дизъюнкты:")
    for clause in simplified_clauses:
        print("  ", clause)

    while True:
        new_clauses = set()
        clauses_list = list(simplified_clauses)

        for i in range(len(clauses_list)):
            for j in range(i+1,len(clauses_list)):
                if i == j:
                    continue
                resolvent = resolve(clauses_list[i], clauses_list[j])
                print(f"Резолюция между {clauses_list[i]} и {clauses_list[j]} -> {resolvent}")

                # Если обнаружен пустой дизъюнкт, возвращаем True
                if isinstance(resolvent, Expression) and isinstance(resolvent.content, Variable) and resolvent.content.name == "⊥":
                    print("Обнаружено противоречие!")
                    return True

                if resolvent is not None:
                    new_clauses.add(resolvent)

        if not new_clauses.difference(simplified_clauses):
            print("Больше новых дизъюнктов нет.")
            break

        print("Новые дизъюнкты:")
        for clause in new_clauses:
            print("  ", clause)

        simplified_clauses.update(new_clauses)

    print("Противоречия не обнаружено.")
    print(simplified_clauses)
    return False





# Пример
A = Variable("A")
B = Variable("B")
C = Variable("C")
D = Variable("D")
E = Variable("E")

#пример с яблоками
clauses = [
    Expression(A),   # X1
    Expression(Implication(A, C)),   #X1 -> X3
    Expression(B), #X2
    Expression(Negation(C))         #not X3
]

print("Противоречивы ли посылки?", check_consistency(clauses))
