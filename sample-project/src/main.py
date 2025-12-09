# Intentionally bad code for SonarQube scanning demonstration
# This file contains bugs, code smells, and poor practices

import os
import sys

# Global variable - code smell
x = 10
y = 20

# Function with a bug - division by zero potential
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    result = total / count  # BUG: Will crash if count is 0
    return result

# Function with code smell - unreadable naming and no documentation
def fn1(a, b, c):
    # This function does something but it's unclear what
    d = a + b
    e = d * c
    f = e - 10
    return f

# Function with security vulnerability - hardcoded password
def authenticate_user(username, password):
    # VULNERABILITY: Hardcoded credentials
    admin_password = "admin123"
    if password == admin_password:
        return True
    return False

# Function with code smell - too many parameters
def process_data(a, b, c, d, e, f, g, h, i, j):
    # Too many parameters - should use a data structure
    result = a + b + c + d + e + f + g + h + i + j
    return result

# Function with bug - unused variable
def unused_variable_example():
    unused_var = 42  # BUG: Variable is never used
    return "hello"

# Function with code smell - magic numbers
def calculate_price(quantity):
    price = quantity * 9.99  # CODE SMELL: Magic number
    tax = price * 0.08  # CODE SMELL: Magic number
    return price + tax

# Function with potential bug - missing error handling
def read_file(filename):
    # BUG: No error handling for file not found
    with open(filename, 'r') as f:
        content = f.read()
    return content

# Function with code smell - duplicate code
def add_numbers(a, b):
    result = a + b
    print(f"Adding {a} and {b}")
    print(f"Result is {result}")
    return result

def subtract_numbers(a, b):
    result = a - b
    print(f"Subtracting {a} and {b}")  # CODE SMELL: Duplicate print pattern
    print(f"Result is {result}")  # CODE SMELL: Duplicate print pattern
    return result

# Function with bug - incorrect logic
def is_even(number):
    # BUG: Logic error - returns True for odd numbers
    if number % 2 == 1:
        return True
    return False

# Main function with code smell - too complex
def main():
    # Too many responsibilities in one function
    numbers = [1, 2, 3, 4, 5]
    avg = calculate_average(numbers)
    print(f"Average: {avg}")
    
    # Empty list will cause division by zero
    empty_list = []
    try:
        avg_empty = calculate_average(empty_list)  # BUG: Will crash
    except:
        pass  # CODE SMELL: Bare except clause
    
    # Using functions with bad names
    result1 = fn1(1, 2, 3)
    print(f"Result: {result1}")
    
    # Security issue
    is_admin = authenticate_user("admin", "admin123")
    print(f"Is admin: {is_admin}")
    
    # Magic numbers
    total = calculate_price(10)
    print(f"Total price: {total}")
    
    # Logic bug
    print(f"Is 4 even? {is_even(4)}")  # Will print False (incorrect)
    print(f"Is 5 even? {is_even(5)}")  # Will print True (incorrect)

if __name__ == "__main__":
    main()

