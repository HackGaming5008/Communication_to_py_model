import re
from fractions import Fraction

def extract_numbers_and_operation(expression):
    # Use regular expression to capture the fractions and operator
    match = re.match(r'(\d+/\d+)\s*([+\-*/])\s*(\d+/\d+)', expression)
    if match:
        num1 = Fraction(match.group(1))
        operator = match.group(2)
        num2 = Fraction(match.group(3))
        return num1, operator, num2
    return None, None, None

def calculate(expression):
    num1, operator, num2 = extract_numbers_and_operation(expression)
    if num1 is None or num2 is None:
        return "Invalid input format."

    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 / num2
    else:
        return "Invalid operator."

# Example usage
expression = "3/4 * 4/5"
result = calculate(expression)
print(f"The result is {result}")
