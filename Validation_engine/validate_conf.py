import os
import json
import yaml
import argparse
from typing import List, Tuple, Dict, Any
from jsonschema import validate, ValidationError

def validate_yaml(fp: str) -> Tuple[bool, str, Any]:
    #validates yaml file, throws exception if pyyaml finds error, for anything else, exception error is thrown
    try:
        with open(fp, 'r', encoding ='utf-8') as file:
            data = yaml.safe_load(file)
        return True, "", data
    except yaml.YAMLError as e:
        return False, f"YAML Error {fp}: {str(e)}", None
    except Exception as e:
        return False, f"Error reading {fp}: {str(e)}", None
    
def validate_json(fp: str) -> Tuple[bool, str, Any]:
    try:
        with open(fp, 'r', encoding ='utf-8') as file:
            data = json.load(file)
        return True, "", data
    except json.JSONDecodeError as e:
        return False, f"JSON Error in {fp}: {str(e)}", None
    except Exception as e:
        return False, f"Error reading {fp}: {str(e)}", None
    


def load_schema_file(schema_path: str) -> Tuple[bool, str, Dict[Any, Any]]:
    """
    Load and validate the schema file's syntax using validate_yaml/validate_json.
    Returns (is_valid, error_message, schema_data)
    """
    # First validate the schema file syntax using existing functions
    if schema_path.endswith(('.yml', '.yaml')):
        is_valid, error_message, schema_data = validate_yaml(schema_path)
    else:  # .json
        is_valid, error_message, schema_data = validate_json(schema_path)
    
    if not is_valid:
        return False, error_message, {}
    
    return True, "", schema_data

def load_config_file(config_path: str) -> Tuple[bool, str, Dict[Any, Any]]:
    """
    Load and validate the config file's syntax using validate_yaml/validate_json.
    Returns (is_valid, error_message, config_data)
    """
    # First validate the config file syntax using existing functions
    if config_path.endswith(('.yml', '.yaml')):
        is_valid, error_message, config_data = validate_yaml(config_path)
    else:  # .json
        is_valid, error_message, config_data = validate_json(config_path)
    
    if not is_valid:
        return False, error_message, {}
    
    return True, "", config_data

def validate_config_against_schema(config_data: Dict[Any, Any], schema_data: Dict[Any, Any]) -> Tuple[bool, str]:
    """
    Validate the config data against the schema using JSON Schema.
    Returns (is_valid, error_message)
    """
    try:
        validate(instance=config_data, schema=schema_data)
        return True, ""
    except ValidationError as e:
        return False, f"Schema validation error: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error during schema validation: {str(e)}"

def validate_file_with_schema(fp: str, schema_path: str) -> Tuple[bool, str]:
    """
    Validate a file's syntax first, then validate against schema.
    Returns (is_valid, error_message)
    """
    # Load schema file
    schema_valid, schema_error, schema_data = load_schema_file(schema_path)
    if not schema_valid:
        return False, f"Schema file validation failed: {schema_error}"
    
    # Load config file
    config_valid, config_error, config_data = load_config_file(fp)
    if not config_valid:
        return False, f"Config file validation failed: {config_error}"
    
    # Validate config against schema
    validation_valid, validation_error = validate_config_against_schema(config_data, schema_data)
    if not validation_valid:
        return False, f"Schema validation error: {validation_error}"
    
    return True, ""

def validate_directory(directory: str, schema_path: str, max_depth: int = None) -> List[Tuple[str, bool, str]]:
    """
    Validate all YAML/JSON files up to max_depth levels below `directory` against the schema.
    If max_depth is None, recurse fully.
    """
    base_depth = directory.rstrip(os.sep).count(os.sep)
    results = []

    for root, dirs, files in os.walk(directory):
        # recursively go through all files in directory and subdirectories
        depth = root.count(os.sep) - base_depth
        if max_depth is not None and depth > max_depth:
            # don't descend further into this subtree
            # by clearing the list of subdirectories
            dirs[:] = []
            continue

        for file in files:
            if file.endswith(('.yml', '.yaml', '.json')):
                file_path = os.path.join(root, file)
                # Validate both syntax and schema
                is_valid, error_message = validate_file_with_schema(file_path, schema_path)
                results.append((file_path, is_valid, error_message))

    return results

def main():
    """
    Define what command-line arguments your program accepts (flags, options, positional arguments).

    Parse the user's input (e.g. sys.argv) into Python objects.

    Automatically generate --help/-h messages and usage summaries.
    """
    parser = argparse.ArgumentParser(description = "Validate YAML/JSON files against schema")
    parser.add_argument("path", help = "Path to the directory or file to validate")
    parser.add_argument("schema", help = "Path to schema file for validation")
    parser.add_argument("-d", "--depth", type = int, help = "Maximum depth to recurse")
    args = parser.parse_args()
    path = args.path
    schema_path = args.schema

    
    if os.path.isfile(path):
        # Validate both syntax and schema
        is_valid, error_message = validate_file_with_schema(path, schema_path)
        if is_valid:
            print(f"File {path} is valid (syntax and schema)")
        else:
            print(f"File {path} is invalid: {error_message}")
    elif os.path.isdir(path):
        results = validate_directory(path, schema_path, args.depth)
        if not results:
            print("No valid files found")
            return
        
        valid_files = 0

        for file_path, is_valid, error_message in results:
            if is_valid:
                print(f"Valid (syntax and schema) file: {file_path}")
                valid_files += 1
            else:
                print(f"Invalid file: {file_path}")
                print(f"Error: {error_message}")

        print(f"\nSummary: {valid_files} files with valid syntax and schema, {len(results) - valid_files} invalid files")
    else:
        print(f"Invalid path: {path}")

if __name__ == "__main__":
    main()

