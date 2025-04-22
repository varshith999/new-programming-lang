import re

# Define token patterns
TOKEN_PATTERNS = [
    (r"Set", "SET"),
    (r"to", "TO"),
    (r"Print", "PRINT"),
    (r"If", "IF"),
    (r"Repeat", "REPEAT"),
    (r"times", "TIMES"),
    (r">", "GREATER"),
    (r"<", "LESS"),
    (r"==", "EQUAL"),
    (r"\+", "PLUS"),
    (r"-", "MINUS"),
    (r"\*", "MULTIPLY"),
    (r"/", "DIVIDE"),
    (r"Define", "DEFINE"),
    (r"->", "ARROW"),
    (r"[a-zA-Z_][a-zA-Z0-9_]*", "IDENTIFIER"),
    (r"\d+", "NUMBER"),
    (r"\s+", None),  # Ignore spaces
]

# Store variables
variables = {}


def tokenize(code):
    tokens = []
    while code:
        match = None
        for pattern, token_type in TOKEN_PATTERNS:
            regex = re.match(pattern, code)
            if regex:
                match = regex.group(0)
                if token_type:  # Ignore spaces
                    tokens.append((token_type, match))
                break
        if not match:
            raise SyntaxError(f"Unexpected token: {code[0]}")
        code = code[len(match):]  # Move to the next part of the code
    return tokens

def evaluate_expression(tokens, start_index):
    """ Evaluate simple expressions like x + 5 """
    if tokens[start_index][0] == "NUMBER":
        return int(tokens[start_index][1]), start_index + 1
    elif tokens[start_index][0] == "IDENTIFIER":
        var_name = tokens[start_index][1]
        if var_name in variables:
            return variables[var_name], start_index + 1
        else:
            raise ValueError(f"Error: Variable '{var_name}' not defined!")
    raise ValueError("Invalid expression!")

def parse(tokens):
    global variables

    if not tokens:
        return "Error: No tokens to parse!"

    index = 0
    while index < len(tokens):
        token_type, token_value = tokens[index]

        # Assignment: "Set x to 10"
        if token_type == "SET":
            if index + 2 < len(tokens) and tokens[index+1][0] == "IDENTIFIER" and tokens[index+2][0] == "TO":
                var_name = tokens[index+1][1]
                value, new_index = evaluate_expression(tokens, index+3)
                variables[var_name] = value
                print(f"(Stored: {var_name} = {value})")
                index = new_index
            else:
                print("Syntax Error: Invalid assignment statement!")

        # Print: "Print x"
        elif token_type == "PRINT":
            if index + 1 < len(tokens) and tokens[index+1][0] == "IDENTIFIER":
                var_name = tokens[index+1][1]
                if var_name in variables:
                    print(f"Output: {variables[var_name]}")
                else:
                    print(f"Error: Variable '{var_name}' is not defined!")
                index += 2
            else:
                print("Syntax Error: Invalid print statement!")

        # If condition: "If x > 5 Print x"
        elif token_type == "IF":
            if index + 3 < len(tokens):
                var_name = tokens[index+1][1]
                operator = tokens[index+2][0]
                value, new_index = evaluate_expression(tokens, index+3)

                if var_name in variables:
                    var_value = variables[var_name]
                    condition_met = False

                    if operator == "GREATER" and var_value > value:
                        condition_met = True
                    elif operator == "LESS" and var_value < value:
                        condition_met = True
                    elif operator == "EQUAL" and var_value == value:
                        condition_met = True

                    if not condition_met:
                        index = len(tokens)  # Skip the next command if condition is false
                else:
                    print(f"Error: Variable '{var_name}' not defined!")

            else:
                print("Syntax Error: Invalid If condition!")

        # Repeat loop: "Repeat 3 times Print x"
        elif token_type == "REPEAT":
            if index + 2 < len(tokens) and tokens[index+1][0] == "NUMBER" and tokens[index+2][0] == "TIMES":
                loop_count = int(tokens[index+1][1])
                loop_start = index + 3  # Start of the loop body

                if loop_start < len(tokens):
                    for _ in range(loop_count):
                        parse(tokens[loop_start:])  # Re-run the loop body
                index = len(tokens)  # Skip remaining tokens after loop execution
            else:
                print("Syntax Error: Invalid Repeat loop!")

        else:
            print(f"Syntax Error: Unexpected token {token_value}")
            break  # Stop on error

    return "Parsing complete!"


# Example input code
code = """
Set x to 5
Repeat 3 times Print x
"""

tokens = tokenize(code)
print("Tokens:", tokens)
parse(tokens)
