# This file contains intentionally bad code to test SonarQube quality gate
# It should fail the quality gate check

def bad_function():
    # Unused variable
    unused = 42
    
    # Division by zero potential
    numbers = []
    result = sum(numbers) / len(numbers)  # Will crash
    
    # Hardcoded password
    password = "admin123"
    
    # Too many parameters
    def too_many_params(a, b, c, d, e, f, g, h, i, j, k, l):
        return a + b + c + d + e + f + g + h + i + j + k + l
    
    # Bare except
    try:
        x = 1 / 0
    except:
        pass
    
    return result

