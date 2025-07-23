import os
import json
import yaml
import argparse
from typing import List, Tuple, Dict, Any
from jsonschema import validate, ValidationError


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



def validate_content_with_schema(config_content: str, schema_content: str) -> Tuple[bool, str]:
    """
    Validate config and schema provided as strings (JSON or YAML).
    Returns (is_valid, error_message)
    """
    def load_content(content: str) -> Tuple[bool, str, Any]:
        # Try JSON first
        try:
            data = json.loads(content)
            return True, "", data
        except json.JSONDecodeError:
            pass
        # Try YAML
        try:
            data = yaml.safe_load(content)
            return True, "", data
        except yaml.YAMLError as e:
            return False, f"YAML Error: {str(e)}", None
        except Exception as e:
            return False, f"Error loading content: {str(e)}", None

    # Load schema content
    schema_valid, schema_error, schema_data = load_content(schema_content)
    if not schema_valid:
        return False, f"Schema content validation failed: {schema_error}"
    # Load config content
    config_valid, config_error, config_data = load_content(config_content)
    if not config_valid:
        return False, f"Config content validation failed: {config_error}"
    # Validate config against schema
    validation_valid, validation_error = validate_config_against_schema(config_data, schema_data)
    if not validation_valid:
        return False, f"Schema validation error: {validation_error}"
    return True, ""

