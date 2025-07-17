import os
import json
from typing import Dict, List, Any, Optional, Union
from openai import OpenAI





class CodeAnalyzer:
    """Analyzes code using OpenAI API to extract functions, methods, classes, and their details."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the CodeAnalyzer.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY.
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)

    def _detect_language_with_gpt(self, code: str) -> str:
        """
        Use GPT to detect the programming language of the code.
        
        Args:
            code: The code snippet to analyze
            
        Returns:
            str: Detected programming language (e.g., 'python', 'javascript', etc.)
        """
        prompt = f"""
        Analyze the following code and determine the programming language.
        
        Code:
        {code}
        
        Return ONLY the language name in lowercase (e.g., 'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'csharp', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin').
        If you cannot determine the language, return 'unknown'.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a programming language detection expert. Return only the language name in lowercase."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=50
            )
            
            language = response.choices[0].message.content.strip().lower()
            
            # Clean up the response to ensure it's a valid language name
            valid_languages = {
                'python', 'javascript', 'typescript', 'java', 'cpp', 'c', 'csharp', 
                'go', 'rust', 'php', 'ruby', 'swift', 'kotlin', 'jsx', 'tsx'
            }
            
            if language in valid_languages:
                return language
            else:
                return 'unknown'
                
        except Exception as e:
            print(f"Language detection error: {e}")
            return 'unknown'
    
    def _analyze_with_openai(self, code: str) -> Dict[str, Any]:
        """Use OpenAI API to get detailed analysis of the code."""

        # Detect language using GPT
        language = self._detect_language_with_gpt(code)
        print(f"Detected language: {language}")

        prompt = f"""
        Analyze the following {language} code and provide detailed information about:
        1. All functions and their parameters, return types, and purpose
        2. All classes, their methods, attributes, and inheritance
        3. Any complex logic or patterns used
        4. Potential issues or improvements
        
        Code:
        {code}
        
        Please provide your analysis in JSON format with the following structure:
        If the code does not use classes or certain structures or if analyzing a functional language, describe modules, main data structures, and key functions instead of classes.
        {{
            "functions": [
                {{
                    "name": "function_name",
                    "description": "what the function does",
                    "parameters": [
                        {{
                            "name": "param_name",
                            "type": "param_type",
                            "description": "what the parameter is for"
                        }}
                    ],
                    "return_type": "return_type",
                    "return_description": "what the function returns",
                    "complexity": "simple/medium/complex"
                }}
            ],
            "classes": [
                {{
                    "name": "class_name",
                    "description": "what the class represents",
                    "methods": [
                        {{
                            "name": "method_name",
                            "description": "what the method does",
                            "parameters": [...],
                            "return_type": "return_type",
                            "return_description": "what the method returns"
                        }}
                    ],
                    "attributes": [
                        {{
                            "name": "attr_name",
                            "type": "attr_type",
                            "description": "what the attribute stores"
                        }}
                    ],
                    "inheritance": "base classes if any"
                }}
            ],
            "overall_complexity": "simple/medium/complex"
            
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a code analysis expert. Provide detailed, accurate analysis of code structure and functionality."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=2000
            )
            
            # Parse the JSON response
            analysis_text = response.choices[0].message.content
            return json.loads(analysis_text)
        
        except Exception as e:
            return {"error": f"OpenAI API error: {str(e)}"}

    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze code and return detailed information.
        
        Args:
            code: The code to analyze
            
        Returns:
            Dictionary containing analysis results
        """
        if not code.strip():
            return {"error": "Empty code provided"}
        
        # Get detailed analysis from OpenAI
        analysis = self._analyze_with_openai(code)
        
        # Add some basic statistics
        if "error" not in analysis:
            functions = analysis.get("functions", [])
            classes = analysis.get("classes", [])
            
            # Calculate statistics
            total_methods = sum(len(cls.get("methods", [])) for cls in classes)
            
            statistics = {
                "total_functions": len(functions),
                "total_classes": len(classes),
                "total_methods": total_methods,
                "overall_complexity": analysis.get("overall_complexity", "unknown")
            }
            
            analysis["statistics"] = statistics
        
        return analysis

    def analyze_file(self, file_path: str) -> Dict[str, Any]:
        """
        Analyze a code file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            Analysis results
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
            
            return self.analyze_code(code)
        
        except Exception as e:
            return {"error": f"File reading error: {str(e)}"}

    def generate_report(self, analysis: Dict[str, Any], format_type: str = "text") -> str:
        """
        Generate a report from the analysis results.
        
        Args:
            analysis: Analysis results from analyze_code
            format_type: "text", "html", or "json"
            
        Returns:
            Formatted report string
        """
        if "error" in analysis:
            return f"Error: {analysis['error']}"
        
        if format_type == "json":
            return json.dumps(analysis, indent=2)
        
        elif format_type == "html":
            return self._generate_html_report(analysis)
        
        else:  # text format
            return self._generate_text_report(analysis)
    
    def _generate_text_report(self, analysis: Dict[str, Any]) -> str:
        """Generate a text report from analysis results."""
        report = []
        report.append("CODE ANALYSIS REPORT")
        report.append("=" * 50)
        
        # Statistics
        stats = analysis.get("statistics", {})
        report.append(f"Total Functions: {stats.get('total_functions', 0)}")
        report.append(f"Total Classes: {stats.get('total_classes', 0)}")
        report.append(f"Total Methods: {stats.get('total_methods', 0)}")
        report.append(f"Overall Complexity: {stats.get('overall_complexity', 'unknown')}")
        report.append("")
        
        # Functions
        functions = analysis.get("functions", [])
        if functions:
            report.append("FUNCTIONS:")
            report.append("-" * 20)
            for func in functions:
                report.append(f"Name: {func.get('name', 'Unknown')}")
                report.append(f"Description: {func.get('description', 'No description')}")
                report.append(f"Return Type: {func.get('return_type', 'Unknown')}")
                
                params = func.get("parameters", [])
                if params:
                    report.append("Parameters:")
                    for param in params:
                        report.append(f"  - {param.get('name', 'Unknown')}: {param.get('type', 'Unknown')} - {param.get('description', 'No description')}")
                
                report.append(f"Complexity: {func.get('complexity', 'Unknown')}")
                report.append("")
        
        # Classes
        classes = analysis.get("classes", [])
        if classes:
            report.append("CLASSES:")
            report.append("-" * 20)
            for cls in classes:
                report.append(f"Name: {cls.get('name', 'Unknown')}")
                report.append(f"Description: {cls.get('description', 'No description')}")
                
                methods = cls.get("methods", [])
                if methods:
                    report.append("Methods:")
                    for method in methods:
                        report.append(f"  - {method.get('name', 'Unknown')}: {method.get('description', 'No description')}")
                
                attributes = cls.get("attributes", [])
                if attributes:
                    report.append("Attributes:")
                    for attr in attributes:
                        report.append(f"  - {attr.get('name', 'Unknown')}: {attr.get('type', 'Unknown')} - {attr.get('description', 'No description')}")
                
                if cls.get("inheritance"):
                    report.append(f"Inheritance: {cls.get('inheritance')}")
                
                report.append("")
        
        return "\n".join(report)
    
    def _generate_html_report(self, analysis: Dict[str, Any]) -> str:
        """Generate an HTML report from analysis results."""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Code Analysis Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background-color: #f0f0f0; padding: 10px; border-radius: 5px; }
                .section { margin: 20px 0; }
                .function, .class { border: 1px solid #ddd; margin: 10px 0; padding: 10px; border-radius: 5px; }
                .parameter { margin-left: 20px; }
                .method, .attribute { margin-left: 20px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Code Analysis Report</h1>
        """
        
        # Statistics
        stats = analysis.get("statistics", {})
        html += f"""
                <p><strong>Total Functions:</strong> {stats.get('total_functions', 0)}</p>
                <p><strong>Total Classes:</strong> {stats.get('total_classes', 0)}</p>
                <p><strong>Total Methods:</strong> {stats.get('total_methods', 0)}</p>
                <p><strong>Overall Complexity:</strong> {stats.get('overall_complexity', 'unknown')}</p>
            </div>
        """
        
        # Functions
        functions = analysis.get("functions", [])
        if functions:
            html += '<div class="section"><h2>Functions</h2>'
            for func in functions:
                html += f"""
                <div class="function">
                    <h3>{func.get('name', 'Unknown')}</h3>
                    <p><strong>Description:</strong> {func.get('description', 'No description')}</p>
                    <p><strong>Return Type:</strong> {func.get('return_type', 'Unknown')}</p>
                """
                
                params = func.get("parameters", [])
                if params:
                    html += '<p><strong>Parameters:</strong></p>'
                    for param in params:
                        html += f'<div class="parameter">• {param.get("name", "Unknown")}: {param.get("type", "Unknown")} - {param.get("description", "No description")}</div>'
                
                html += f'<p><strong>Complexity:</strong> {func.get("complexity", "Unknown")}</p></div>'
            html += '</div>'
        
        # Classes
        classes = analysis.get("classes", [])
        if classes:
            html += '<div class="section"><h2>Classes</h2>'
            for cls in classes:
                html += f"""
                <div class="class">
                    <h3>{cls.get('name', 'Unknown')}</h3>
                    <p><strong>Description:</strong> {cls.get('description', 'No description')}</p>
                """
                
                methods = cls.get("methods", [])
                if methods:
                    html += '<p><strong>Methods:</strong></p>'
                    for method in methods:
                        html += f'<div class="method">• {method.get("name", "Unknown")}: {method.get("description", "No description")}</div>'
                
                attributes = cls.get("attributes", [])
                if attributes:
                    html += '<p><strong>Attributes:</strong></p>'
                    for attr in attributes:
                        html += f'<div class="attribute">• {attr.get("name", "Unknown")}: {attr.get("type", "Unknown")} - {attr.get("description", "No description")}</div>'
                
                if cls.get("inheritance"):
                    html += f'<p><strong>Inheritance:</strong> {cls.get("inheritance")}</p>'
                
                html += '</div>'
            html += '</div>'
        
        html += """
        </body>
        </html>
        """
        
        return html

    def save_tests_to_file(self, analysis: Dict[str, Any], filename: str):
        """Save analysis results to a JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analysis, f, indent=2, ensure_ascii=False)
            print(f"Analysis saved to {filename}")
        except Exception as e:
            print(f"Error saving file: {e}")
    
