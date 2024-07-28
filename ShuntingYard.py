def get_precedence(op):
    precedences = {'(': 1, '|': 2, '.': 3, '?': 4, '*': 4, '+': 4, '^': 5}
    return precedences.get(op, -1)

def format_reg_ex(regex):
    all_operators = {'|', '?', '+', '*', '^', '.'}
    binary_operators = {'^', '|'}
    res = ""
    i = 0
    
    while i < len(regex):
        c1 = regex[i]
        if c1 == '\\':
            
            res += regex[i:i+2]
            i += 2  
            continue
        res += c1
        if i + 1 < len(regex):
            c2 = regex[i + 1]
            if (c1 != '(' and c2 != ')' and
                c2 not in all_operators and
                c1 not in binary_operators and
                not (c1 == '\\' or c2 == '\\')):
                res += '.'
        i += 1
                
    return res

def infix_to_postfix(regex):
    formatted_regex = format_reg_ex(regex)
    stack = []
    postfix = ""
    steps = []  

    i = 0
    while i < len(formatted_regex):
        c = formatted_regex[i]
        if c == '\\':
            postfix += formatted_regex[i:i+2]
            steps.append(f"Se agrega el caracter escapado {formatted_regex[i:i+2]} a la salida")
            i += 2
            continue
        if c == '(':
            stack.append(c)
            steps.append("Se mueve '(' al stack")
        elif c == ')':
            while stack and stack[-1] != '(':
                steps.append(f"Se borra {stack[-1]} del stack")
                postfix += stack.pop()
            if stack:  # Verificación adicional antes de hacer pop de '('
                stack.pop()
                steps.append("Se borra '(' del stack")
            else:
                steps.append("Error: Stack vacío al intentar pop de '('")
        else:
            while stack and get_precedence(stack[-1]) >= get_precedence(c):
                steps.append(f"Se borra {stack[-1]} del stack")
                postfix += stack.pop()
            stack.append(c)
            steps.append(f"Se mueve '{c}' al stack")
        i += 1
    
    while stack:
        steps.append(f"Se borra {stack[-1]} del stack")
        postfix += stack.pop()

    return postfix, steps

def process_file(file_path):
    results = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:
                postfix, steps = infix_to_postfix(line)
                results.append((line, postfix, steps))
    return results

results = process_file('expressions.txt')
for original, postfix, step_list in results:
    print(f"Original: {original} -> Postfix: {postfix}")
    for step in step_list:
        print(step)
    print("\n---\n")
