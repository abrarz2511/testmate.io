# Configuration Validation Tool

This repository contains a Python script for validating configuration files against schemas with both syntax and semantic validation:

- `validate_conf.py` - Complete validation script with syntax and schema validation

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

The script validates YAML/JSON files against a schema file. Both syntax and semantic validation are performed.

```bash
# Validate a single file against a schema
python validate_conf.py config.json schema.json

# Validate all files in a directory against a schema
python validate_conf.py /path/to/configs/ schema.json

# Validate with depth limit
python validate_conf.py /path/to/configs/ schema.json -d 2
```

## Examples

### Valid Configuration

```bash
python validate_conf.py example_config.json example_schema.json
```

Expected output:

```
File example_config.json is valid (syntax and schema)
```

### Invalid Configuration

```bash
python validate_conf.py example_invalid_config.json example_schema.json
```

Expected output:

```
File example_invalid_config.json is invalid: Schema validation error: 'invalid-version' does not match '^\\d+\\.\\d+\\.\\d+$'
```

### Directory Validation

```bash
python validate_conf.py . example_schema.json
```

Expected output:

```
Valid (syntax and schema) file: ./example_config.json
Invalid file: ./example_invalid_config.json
Error: Schema validation error: 'invalid-version' does not match '^\\d+\\.\\d+\\.\\d+$'

Summary: 1 files with valid syntax and schema, 1 invalid files
```

## Features

- **Integrated Validation**: Single script handles both syntax and schema validation
- **Syntax Validation**: Validates YAML/JSON file syntax using dedicated functions
- **Schema Validation**: Uses JSON Schema standard for comprehensive validation
- **Multiple Formats**: Supports both JSON and YAML files for both config and schema
- **Error Reporting**: Detailed error messages for debugging
- **Command Line Interface**: Easy to use from command line or integrate into scripts
- **Directory Recursion**: Can validate entire directories with optional depth limits

## Command Line Options

- `path`: Path to file or directory to validate
- `schema`: Path to schema file for validation (required)
- `-d, --depth`: Maximum depth to recurse when validating directories

## File Structure

```
├── validate_conf.py              # Complete validation script
├── requirements.txt              # Python dependencies
├── example_schema.json          # Example JSON schema
├── example_config.json          # Example valid config
├── example_invalid_config.json  # Example invalid config
└── README.md                    # This file
```

## How It Works

1. **Schema Loading**: Loads and validates the schema file's syntax
2. **Config Loading**: Loads and validates the config file's syntax
3. **Schema Validation**: Validates the config data against the schema using JSON Schema
4. **Error Handling**: Provides clear error messages for both syntax and schema validation failures

## Validation Process

The script performs validation in the following order:

1. **Schema File Syntax**: Validates the schema file using `validate_yaml` or `validate_json`
2. **Config File Syntax**: Validates the config file using `validate_yaml` or `validate_json`
3. **Schema Validation**: Uses JSON Schema to validate the config against the schema
4. **Result Reporting**: Reports success or detailed error messages
