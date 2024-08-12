import math
import re


from fractions import Fraction



def extract_numbers_and_operation(pattern):
    # Regex pattern to match basic math operations
    if isinstance(pattern, list):
        pattern = ' '.join(pattern) 

    match = re.search(r'(\d+)\s*(plus|add|\+|minus|subtract|\-|times|multiply|\*|divide|\/)\s*(\d+)', pattern, re.IGNORECASE)
    if match:
        num1 = float(match.group(1))
        operation = match.group(2)  # Operation should be captured
        num2 = float(match.group(3))
        return num1, operation, num2
    return None, None, None


def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y != 0:
        return x / y
    else:
        return "Cannot divide by zero."

def extract_numbers_for_fraction(sentence):

    if isinstance(sentence, list):
        sentence = ' '.join(sentence) 
    # Regex to capture fractions and operation
    pattern = r'(\d+/\d+)\s*(plus|add|\+|minus|subtract|-|times|multiply|\*|divided by|divide|/)\s*(\d+/\d+)'
    match = re.search(pattern, sentence)
    if match:
        num1 = match.group(1)
        operation = match.group(2)
        num2 = match.group(3)
        return num1, operation, num2
    return None, None, None


def calculate_fraction(num1, operation, num2):
    try:
        # Convert inputs to Fraction objects
        frac1 = Fraction(num1)
        frac2 = Fraction(num2)
        
        # Perform calculation
        if operation in ['plus', 'add', '+']:
            result = frac1 + frac2
        elif operation in ['minus', 'subtract', '-']:
            result = frac1 - frac2
        elif operation in ['times', 'multiply', '*']:
            result = frac1 * frac2
        elif operation in ['divide', 'divided by', '/']:
            result = frac1 / frac2
        else:
            return "Operation not recognized."
        
        return f"The result is {result}"
    
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error during calculation: {e}"