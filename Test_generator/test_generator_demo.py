#!/usr/bin/env python3
"""
Demo script to test the TestGenerator functionality.
This script demonstrates how to use the TestGenerator with different types of code.
"""

import os
import json
from generate_tests import TestGenerator


def test_python_code():
    """Test with Python code."""
    print("=" * 50)
    print("Testing Python Code Generation")
    print("=" * 50)
    
    python_code = """
def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

class MathUtils:
    def __init__(self):
        self.calculations = []
    
    def add(self, a: float, b: float) -> float:
        result = a + b
        self.calculations.append(f"{a} + {b} = {result}")
        return result
    
    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.calculations.append(f"{a} * {b} = {result}")
        return result
    
    def get_calculations(self) -> list:
        return self.calculations
"""
    
    try:
        generator = TestGenerator()
        tests = generator.generate_tests(python_code)
        
        if "error" in tests:
            print(f"Error: {tests['error']}")
        else:
            print("✓ Python test generation successful!")
            print(f"Generated {len(tests.get('test_suite', []))} test suites")
            
            # Save to file
            generator.save_tests_to_file(tests, "python_tests.json")
            print("✓ Tests saved to 'python_tests.json'")
            
    except Exception as e:
        print(f"✗ Error testing Python code: {e}")


def test_javascript_code():
    """Test with JavaScript code."""
    print("\n" + "=" * 50)
    print("Testing JavaScript Code Generation")
    print("=" * 50)
    
    javascript_code = """
function calculateFactorial(n) {
    if (n <= 1) return 1;
    return n * calculateFactorial(n - 1);
}

function isPalindrome(str) {
    const cleaned = str.toLowerCase().replace(/[^a-z0-9]/g, '');
    return cleaned === cleaned.split('').reverse().join('');
}

class StringUtils {
    constructor() {
        this.operations = [];
    }
    
    reverse(str) {
        const result = str.split('').reverse().join('');
        this.operations.push(`reverse("${str}") = "${result}"`);
        return result;
    }
    
    countWords(str) {
        const words = str.trim().split(/\\s+/);
        const count = words.length;
        this.operations.push(`countWords("${str}") = ${count}`);
        return count;
    }
    
    getOperations() {
        return this.operations;
    }
}
"""
    
    try:
        generator = TestGenerator()
        tests = generator.generate_tests(javascript_code)
        
        if "error" in tests:
            print(f"Error: {tests['error']}")
        else:
            print("✓ JavaScript test generation successful!")
            print(f"Generated {len(tests.get('test_suite', []))} test suites")
            
            # Save to file
            generator.save_tests_to_file(tests, "javascript_tests.json")
            print("✓ Tests saved to 'javascript_tests.json'")
            
    except Exception as e:
        print(f"✗ Error testing JavaScript code: {e}")


def test_file_processing():
    """Test generating tests from a file."""
    print("\n" + "=" * 50)
    print("Testing File Processing")
    print("=" * 50)
    
    # Create a temporary test file
    test_file_content = """
def validate_email(email: str) -> bool:
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
    import re
    pattern = r'^\\+?1?\\s*\\(?[0-9]{3}\\)?[-\\s]?[0-9]{3}[-\\s]?[0-9]{4}$'
    return bool(re.match(pattern, phone))

class UserValidator:
    def __init__(self):
        self.validation_history = []
    
    def validate_user(self, email: str, phone: str) -> dict:
        email_valid = validate_email(email)
        phone_valid = validate_phone(phone)
        
        result = {
            'email_valid': email_valid,
            'phone_valid': phone_valid,
            'all_valid': email_valid and phone_valid
        }
        
        self.validation_history.append(result)
        return result
    
    def get_history(self) -> list:
        return self.validation_history
"""
    
    # Write test file
    with open("temp_test_file.py", "w") as f:
        f.write(test_file_content)
    
    try:
        generator = TestGenerator()
        tests = generator.generate_tests_for_file("temp_test_file.py")
        
        if "error" in tests:
            print(f"Error: {tests['error']}")
        else:
            print("✓ File processing successful!")
            print(f"Generated {len(tests.get('test_suite', []))} test suites")
            
            # Save to file
            generator.save_tests_to_file(tests, "file_tests.json")
            print("✓ Tests saved to 'file_tests.json'")
            
    except Exception as e:
        print(f"✗ Error testing file processing: {e}")
    finally:
        # Clean up
        if os.path.exists("temp_test_file.py"):
            os.remove("temp_test_file.py")


def test_error_handling():
    """Test error handling with invalid code."""
    print("\n" + "=" * 50)
    print("Testing Error Handling")
    print("=" * 50)
    
    invalid_code = """
This is not valid code at all!
It has syntax errors and invalid syntax.
"""
    
    try:
        generator = TestGenerator()
        tests = generator.generate_tests(invalid_code)
        
        if "error" in tests:
            print("✓ Error handling working correctly!")
            print(f"Error message: {tests['error']}")
        else:
            print("⚠ Unexpected: No error detected for invalid code")
            
    except Exception as e:
        print(f"✗ Unexpected exception: {e}")


def main():
    """Run all tests."""
    print("Test Generator Demo")
    print("This script will test the TestGenerator with different types of code.")
    print("Make sure you have set the OPENAI_API_KEY environment variable.")
    print()
    
    # Check if API key is available
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠ Warning: OPENAI_API_KEY environment variable not set!")
        print("   Set it with: export OPENAI_API_KEY='your-api-key-here'")
        print("   Or the script will fail when trying to connect to OpenAI API.")
        print()
    
    # Run tests
    test_python_code()
    test_javascript_code()
    test_file_processing()
    test_error_handling()
    
    print("\n" + "=" * 50)
    print("Demo completed!")
    print("Check the generated JSON files for the test results.")
    print("=" * 50)


if __name__ == "__main__":
    main() 