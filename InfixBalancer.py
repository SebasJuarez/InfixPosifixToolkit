def is_balanced(expression):
    stack = []
    matching_bracket = {')': '(', ']': '[', '}': '{'}
    steps = []

    for char in expression:
        if char in matching_bracket.values():
            stack.append(char)
            steps.append(f"Se añade '{char}' a la pila: {stack}")
        elif char in matching_bracket:
            if stack and stack[-1] == matching_bracket[char]:
                steps.append(f"Se saca '{stack.pop()}' de la pila porque coincide con '{char}': {stack}")
            else:
                steps.append(f"Error: '{char}' no coincide o la pila está vacía: {stack}")
                return False, steps

    if stack:
        steps.append("La pila no está vacía al final de la expresión: {stack}")
        return False, steps
    return True, steps

def process_file(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line_number, line in enumerate(file, 1):
            line = line.strip()
            balanced, steps = is_balanced(line)
            results.append((line_number, line, balanced, steps))
    return results

results = process_file('expressions1.txt')
for line_number, expression, balanced, steps in results:
    estado = 'balanceada' if balanced else 'desbalanceada'
    print(f"Línea {line_number}: '{expression}' está {estado}")
    for step in steps:
        print(step)
    print("\n---\n")
