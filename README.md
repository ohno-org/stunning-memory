# stunning-memory

A Python script to set custom properties on all repositories in a GitHub organization.

## Features

- 🔄 Set custom properties on all repositories in an organization
- 🎯 Filter repositories by name
- 🔍 Dry-run mode to preview changes before applying
- 📝 Support for multiple properties at once
- 📄 Load properties from JSON file
- 🚨 Comprehensive error handling and logging
- ✅ Detailed success/failure reporting

## Prerequisites

- Python 3.7 or higher
- GitHub personal access token with appropriate permissions:
  - `repo` scope (for repository access)
  - `admin:org` scope (for organization-level custom properties)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd stunning-memory
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Set a single custom property on all repositories:
```bash
export GITHUB_TOKEN="your_github_token"
python set_custom_properties.py --org your-org-name --property "team=backend"
```

### Set Multiple Properties

```bash
python set_custom_properties.py \
  --org your-org-name \
  --property "team=backend" \
  --property "environment=production" \
  --property "owner=engineering"
```

### Load Properties from JSON File

Create a JSON file (e.g., `properties.json`):
```json
{
  "team": "platform",
  "environment": "production",
  "owner": "engineering"
}
```

Then run:
```bash
python set_custom_properties.py --org your-org-name --properties-file properties.json
```

### Dry Run Mode

Preview changes without actually applying them:
```bash
python set_custom_properties.py --org your-org-name --property "team=backend" --dry-run
```

### Filter Repositories

Only update repositories whose names contain a specific string:
```bash
python set_custom_properties.py --org your-org-name --property "team=frontend" --filter "frontend"
```

### Command Line Options

```
--token TOKEN              GitHub personal access token (or set GITHUB_TOKEN env var)
--org ORG                  GitHub organization name (required)
--property PROPERTY        Custom property in format "name=value" (can be used multiple times)
--properties-file FILE     JSON file containing properties to set
--dry-run                  Show what would be done without making any changes
--filter FILTER            Filter repositories by name (substring match)
--verbose                  Enable verbose logging
```

## Examples

### Example 1: Set Team Property on All Repos

```bash
python set_custom_properties.py --org myorg --property "team=platform"
```

### Example 2: Set Multiple Properties with Filtering

```bash
python set_custom_properties.py \
  --org myorg \
  --property "team=frontend" \
  --property "stack=react" \
  --filter "web-"
```

### Example 3: Using a Properties File

```bash
python set_custom_properties.py --org myorg --properties-file properties_example.json
```

### Example 4: Dry Run with Verbose Output

```bash
python set_custom_properties.py \
  --org myorg \
  --property "environment=staging" \
  --dry-run \
  --verbose
```

## Authentication

The script requires a GitHub personal access token. You can provide it in two ways:

1. **Environment variable** (recommended):
```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

2. **Command line argument**:
```bash
python set_custom_properties.py --token "ghp_your_token_here" --org myorg --property "team=backend"
```

## Output

The script provides clear logging of its progress:

```
2024-10-14 21:00:00 - INFO - Successfully connected to organization: myorg
2024-10-14 21:00:01 - INFO - Found 25 repositories in myorg
2024-10-14 21:00:02 - INFO - ✓ Set team=backend on myorg/repo1
2024-10-14 21:00:03 - INFO - ✓ Set team=backend on myorg/repo2
...
============================================================
SUMMARY
============================================================
Successfully updated: 25
Failed to update: 0
```

## Error Handling

The script includes comprehensive error handling:
- Validates GitHub token and organization access
- Reports errors for individual repositories without stopping execution
- Provides a summary of successes and failures
- Exits with appropriate status codes for CI/CD integration

## Notes

- Custom properties must be defined at the organization level before they can be set on repositories
- The script uses the GitHub REST API's custom properties endpoint
- Large organizations with many repositories may take some time to process

## License

Apache License 2.0 - See LICENSE file for details.