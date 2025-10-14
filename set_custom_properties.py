#!/usr/bin/env python3
"""
Script to set custom properties on all repositories in a GitHub organization.

This script uses the GitHub REST API to:
1. List all repositories in an organization
2. Set custom properties on each repository

Requirements:
- PyGithub library
- GitHub personal access token with repo and admin:org permissions
"""

import argparse
import json
import logging
import os
import sys
from typing import Dict, List, Optional

try:
    from github import Github, GithubException, Auth
    from github.Repository import Repository
    import requests
except ImportError as e:
    if "github" in str(e):
        print("Error: PyGithub library not found. Install it with: pip install PyGithub")
    else:
        print(f"Error: Required library not found: {e}")
    sys.exit(1)


# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CustomPropertySetter:
    """Class to handle setting custom properties on GitHub repositories."""

    def __init__(self, token: str, org_name: str):
        """
        Initialize the CustomPropertySetter.

        Args:
            token: GitHub personal access token
            org_name: Name of the GitHub organization
        """
        auth = Auth.Token(token)
        self.github = Github(auth=auth)
        self.token = token
        self.org_name = org_name
        self.org = None

    def validate_connection(self) -> bool:
        """
        Validate the GitHub connection and organization access.

        Returns:
            True if connection is valid, False otherwise
        """
        try:
            self.org = self.github.get_organization(self.org_name)
            logger.info(f"Successfully connected to organization: {self.org_name}")
            return True
        except GithubException as e:
            logger.error(f"Failed to connect to organization {self.org_name}: {e}")
            return False

    def get_all_repos(self) -> List[Repository]:
        """
        Get all repositories in the organization.

        Returns:
            List of Repository objects
        """
        try:
            repos = list(self.org.get_repos())
            logger.info(f"Found {len(repos)} repositories in {self.org_name}")
            return repos
        except GithubException as e:
            logger.error(f"Failed to fetch repositories: {e}")
            return []

    def set_custom_property(
        self,
        repo: Repository,
        property_name: str,
        property_value: str
    ) -> bool:
        """
        Set a custom property on a repository using the GitHub REST API.

        Note: Custom properties are set using the REST API endpoint:
        PATCH /repos/{owner}/{repo}/properties/values

        Args:
            repo: Repository object
            property_name: Name of the custom property
            property_value: Value of the custom property

        Returns:
            True if successful, False otherwise
        """
        try:
            # Using direct HTTP request for custom properties API
            url = f"https://api.github.com/repos/{repo.full_name}/properties/values"
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "X-GitHub-Api-Version": "2022-11-28"
            }
            data = {
                "properties": [
                    {
                        "property_name": property_name,
                        "value": property_value
                    }
                ]
            }

            response = requests.patch(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()

            logger.info(
                f"✓ Set {property_name}={property_value} on {repo.full_name}"
            )
            return True

        except requests.exceptions.HTTPError as e:
            # Log only status code to avoid exposing sensitive information
            logger.error(
                f"✗ Failed to set property on {repo.full_name}: HTTP {e.response.status_code}"
            )
            return False
        except requests.exceptions.ConnectionError:
            logger.error(
                f"✗ Connection error setting property on {repo.full_name}"
            )
            return False
        except requests.exceptions.Timeout:
            logger.error(
                f"✗ Request timeout setting property on {repo.full_name}"
            )
            return False
        except requests.exceptions.RequestException as e:
            logger.error(
                f"✗ Request error setting property on {repo.full_name}: {type(e).__name__}"
            )
            return False
        except Exception as e:
            logger.error(
                f"✗ Unexpected error setting property on {repo.full_name}: {type(e).__name__}"
            )
            return False

    def set_properties_on_all_repos(
        self,
        properties: Dict[str, str],
        dry_run: bool = False,
        repo_filter: Optional[str] = None
    ) -> Dict[str, int]:
        """
        Set custom properties on all repositories in the organization.

        Args:
            properties: Dictionary of property names and values
            dry_run: If True, only print what would be done without making changes
            repo_filter: Optional string to filter repository names (substring match)

        Returns:
            Dictionary with success and failure counts
        """
        repos = self.get_all_repos()

        if repo_filter:
            repos = [r for r in repos if repo_filter.lower() in r.name.lower()]
            logger.info(f"Filtered to {len(repos)} repositories matching '{repo_filter}'")

        if dry_run:
            logger.info("DRY RUN MODE - No changes will be made")

        results = {"success": 0, "failed": 0, "skipped": 0}

        for repo in repos:
            if dry_run:
                logger.info(f"[DRY RUN] Would set properties on {repo.full_name}:")
                for prop_name, prop_value in properties.items():
                    logger.info(f"  {prop_name} = {prop_value}")
                results["skipped"] += 1
            else:
                success = True
                for prop_name, prop_value in properties.items():
                    if not self.set_custom_property(repo, prop_name, prop_value):
                        success = False

                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1

        return results


def load_properties_from_file(file_path: str) -> Dict[str, str]:
    """
    Load custom properties from a JSON file.

    Args:
        file_path: Path to the JSON file

    Returns:
        Dictionary of property names and values
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load properties from file {file_path}: {e}")
        sys.exit(1)


def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(
        description="Set custom properties on all repositories in a GitHub organization",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Set a single property on all repos
  python set_custom_properties.py --org myorg --property "team=backend"

  # Set multiple properties
  python set_custom_properties.py --org myorg --property "team=backend" --property "env=prod"

  # Load properties from a JSON file
  python set_custom_properties.py --org myorg --properties-file properties.json

  # Dry run to see what would be changed
  python set_custom_properties.py --org myorg --property "team=backend" --dry-run

  # Filter repositories by name
  python set_custom_properties.py --org myorg --property "team=backend" --filter "frontend"

Environment Variables:
  GITHUB_TOKEN: GitHub personal access token (can be used instead of --token)
        """
    )

    parser.add_argument(
        '--token',
        help='GitHub personal access token (or set GITHUB_TOKEN env var)',
        default=os.environ.get('GITHUB_TOKEN')
    )

    parser.add_argument(
        '--org',
        required=True,
        help='GitHub organization name'
    )

    parser.add_argument(
        '--property',
        action='append',
        dest='properties',
        help='Custom property in format "name=value" (can be used multiple times)'
    )

    parser.add_argument(
        '--properties-file',
        help='JSON file containing properties to set'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be done without making any changes'
    )

    parser.add_argument(
        '--filter',
        help='Filter repositories by name (substring match)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Validate token
    if not args.token:
        logger.error(
            "GitHub token is required. Provide it via --token or GITHUB_TOKEN environment variable"
        )
        sys.exit(1)

    # Parse properties
    properties = {}

    if args.properties_file:
        properties = load_properties_from_file(args.properties_file)

    if args.properties:
        for prop in args.properties:
            prop = prop.strip()
            if not prop:
                logger.error("Empty property provided")
                sys.exit(1)
            if '=' not in prop:
                logger.error(f"Invalid property format: {prop}. Expected 'name=value'")
                sys.exit(1)
            name, value = prop.split('=', 1)
            name = name.strip()
            value = value.strip()
            if not name:
                logger.error(f"Property name cannot be empty in: {prop}")
                sys.exit(1)
            properties[name] = value

    if not properties:
        logger.error(
            "No properties specified. Use --property or --properties-file"
        )
        sys.exit(1)

    logger.info(f"Properties to set: {properties}")

    # Initialize the setter and run
    setter = CustomPropertySetter(args.token, args.org)

    if not setter.validate_connection():
        sys.exit(1)

    results = setter.set_properties_on_all_repos(
        properties,
        dry_run=args.dry_run,
        repo_filter=args.filter
    )

    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    if args.dry_run:
        logger.info(f"Repositories that would be updated: {results['skipped']}")
    else:
        logger.info(f"Successfully updated: {results['success']}")
        logger.info(f"Failed to update: {results['failed']}")

    if results['failed'] > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
