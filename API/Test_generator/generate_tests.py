import os
import json
from typing import Dict, List, Any, Optional, Union
from openai import OpenAI
from .analyze_code import CodeAnalyzer
from dotenv import load_dotenv

load_dotenv()

class TestGenerator: 
    """Generates test cases based on code analysis using OpenAI API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the TestGenerator.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.analyzer = CodeAnalyzer(api_key=self.api_key)

    
    def generate_tests(self, code: str) -> Dict[str, Any]:
        """
        Generate test cases based on code analysis. (Wrapper function)
        
        Args:
            code: The source code to analyze and generate tests for
            
        Returns:
            Dictionary containing test objects with test types and test cases
        """
        # First, analyze the code to understand its structure
        analysis = self.analyzer._analyze_with_openai(code)
        
        if "error" in analysis:
            return {"error": f"Analysis failed: {analysis['error']}"}
        
        # Detect the language of the original code
        language = self.analyzer._detect_language_with_gpt(code)
        
        # Generate tests based on the analysis
        return self._generate_test_cases(analysis, language, code)
    

    def _generate_test_cases(self, analysis: Dict[str, Any], language: str, original_code: str) -> Dict[str, Any]:
        """Generate test cases using OpenAI based on the code analysis."""
        
        # Create a prompt for test generation
        prompt = f"""
        Based on the following code analysis, generate comprehensive test cases in {language}.
        
        Code Analysis:
        {json.dumps(analysis, indent=2)}
        
        Original Code:
        {original_code}
        
        Generate test cases that include:
        1. Unit tests for each function and method
        2. Integration tests for classes and complex interactions
        3. Edge cases and error conditions
        4. Tests for different input scenarios
        
        CRITICAL: You must respond with ONLY valid JSON. Do not include any explanatory text before or after the JSON.
        
        Use this exact JSON structure:
        {{
            "test_suite": [
                {{
                    "test_type": "unit_test",
                    "target": "function_name",
                    "description": "what this test is testing",
                    "test_cases": [
                        {{
                            "name": "test_case_name",
                            "description": "what this specific test case does",
                            "input": "input_data_or_parameters",
                            "expected_output": "expected_result",
                            "test_code": "actual test code in {language}"
                        }}
                    ]
                }}
            ],
            "test_framework": "appropriate testing framework for {language}",
            "setup_instructions": "how to set up the testing environment"
        }}
        
        Make sure the test code is written in {language} and uses appropriate testing conventions for that language.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are a testing expert specializing in {language}. Generate comprehensive, well-structured test cases that follow best practices for {language} testing. IMPORTANT: You must respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            
            # Parse the JSON response
            test_text = response.choices[0].message.content.strip()
            
            # Debug: Print the raw response to see what we're getting
            print(f"Raw API response: {test_text[:200]}...")
            
            if not test_text:
                return {"error": "Empty response from API"}
            
            try:
                return json.loads(test_text)
            except json.JSONDecodeError as json_error:
                return {"error": f"Invalid JSON response from API: {str(json_error)}. Raw response: {test_text[:500]}..."}
        
        except Exception as e:
            return {"error": f"Test generation error: {str(e)}"}
    

    def generate_tests_for_file(self, file_path: str) -> Dict[str, Any]:  # Probably not  needed
        """
        Generate test cases for a code file.
        
        Args:
            file_path: Path to the file to generate tests for
            
        Returns:
            Test generation results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            return self.generate_tests(code)
        
        except Exception as e:
            return {"error": f"File reading error: {str(e)}"}
    

    def save_tests_to_file(self, tests: Dict[str, Any], output_file: str) -> bool:
        """
        Save generated tests to a file.
        
        Args:
            tests: The generated test data
            output_file: Path to save the tests
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tests, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving tests: {str(e)}")
            return False

'''
def main():
    """Example usage of the TestGenerator."""
    # Example code to test
    sample_code = """
function addNumbers(a, b) {
    return a + b;
}

function multiplyNumbers(a, b) {
    return a * b;
}

class Calculator {
    constructor() {
        this.history = [];
    }
    
    add(a, b) {
        const result = a + b;
        this.history.push(`${a} + ${b} = ${result}`);
        return result;
    }
    
    getHistory() {
        return this.history;
    }
}
"""
    
    # Initialize the test generator
    generator = TestGenerator()
    
    # Generate tests
    tests = generator.generate_tests(sample_code)
    
    # Print results
    if "error" in tests:
        print(f"Error: {tests['error']}")
    else:
        print("Generated Tests:")
        print(json.dumps(tests, indent=2))
        
        # Save to file
        generator.save_tests_to_file(tests, "generated_tests.json")
        print("\nTests saved to 'generated_tests.json'")
        


if __name__ == "__main__":
    main() 

'''