class Expression:
    def __init__(self, content):
        """Класс для хранения логического выражения."""
        self.content = content

    def __repr__(self):
        return repr(self.content)

    def substitute(self, var, expr):
        """Заменяет все вхождения переменной var на выражение expr внутри content."""
        return Expression(self.content.substitute(var, expr))


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


class Negation:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"¬{self.expression}"

    def __eq__(self, other):
        return isinstance(other, Negation) and self.expression == other.expression

    def __hash__(self):
        return hash(('¬', self.expression))

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

    def __hash__(self):
        return hash((self.antecedent, '→', self.consequent))

    def substitute(self, var, expr):
        new_antecedent = self.antecedent.substitute(var, expr)
        new_consequent = self.consequent.substitute(var, expr)
        return Implication(new_antecedent, new_consequent)



def remove_redundant(formulas):
    """Удаляет неактуальные формулы, используя известные истинные значения."""
    simplified = []
    known_true = set()

    for formula in formulas:
        if isinstance(formula.content, Negation):
            known_true.add(formula.content.expression)
        elif isinstance(formula.content, Implication):
            if formula.content.consequent in known_true:
                continue
            if formula.content.antecedent in known_true:
                known_true.add(formula.content.consequent)
            else:
                simplified.append(formula)
    return simplified, known_true



def resolution(formulas, max_iterations=1000):
    """Ищет противоречие в наборе посылок с помощью разрешения."""
    iteration = 0
    known_true = set()

    while iteration < max_iterations:
        iteration += 1
        print(f"Итерация {iteration}: текущие формулы - {formulas}")

        # Упрощаем формулы
        formulas, new_true = remove_redundant(formulas)
        known_true.update(new_true)

        # Проверяем на противоречие
        for formula in formulas:
            if isinstance(formula.content, Negation) and formula.content.expression in known_true:
                print("Противоречие найдено!")
                return True

        # Применение транзитивности
        new_formulas = set(formulas)
        resolved = False

        for f1 in formulas:
            for f2 in formulas:
                if isinstance(f1.content, Implication) and isinstance(f2.content, Implication):
                    # A → B и B → C дают A → C
                    if f1.content.consequent == f2.content.antecedent:
                        new_formula = Expression(Implication(f1.content.antecedent, f2.content.consequent))
                        if new_formula not in new_formulas:
                            new_formulas.add(new_formula)
                            resolved = True

        # Если новых формул нет, завершаем работу
        if not resolved:
            print("Противоречие не найдено после", iteration, "итераций.")
            break

        # Обновляем формулы для следующей итерации
        formulas = list(new_formulas)

    # Противоречие не найдено
    return False


# Пример использования:

# Определяем переменные
A = Variable("A")
B = Variable("B")
C = Variable("C")
D = Variable("D")
E = Variable("E")
F = Variable("F")

# Задаем набор посылок
formulas = [
    Expression(Implication(A, B)),
    Expression(Implication(C, D)),
    Expression(Implication(B, Implication(D, E))),
    Expression(Implication(E, F)),
    Expression(Negation(F)),
    Expression(Implication(D, Implication(A, C)))
]

# Проверяем на противоречие
if resolution(formulas):
    print("Противоречие найдено в наборе посылок.")
else:
    print("Противоречие не найдено.")
