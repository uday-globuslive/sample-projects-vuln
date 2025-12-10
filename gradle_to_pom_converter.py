#!/usr/bin/env python3
"""
Gradle to Maven POM Converter
Converts all build.gradle files to pom.xml files recursively in a directory.

Usage:
    python gradle_to_pom_converter.py <path_to_folder>
    python gradle_to_pom_converter.py .
    python gradle_to_pom_converter.py c:\\path\\to\\projects
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class GradleToPomConverter:
    """Convert Gradle build.gradle files to Maven pom.xml files."""

    def __init__(self):
        self.pom_template = '''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>{group_id}</groupId>
    <artifactId>{artifact_id}</artifactId>
    <version>{version}</version>
    <name>{project_name}</name>
    <description>Converted from Gradle build.gradle</description>

    <dependencies>
{dependencies}
    </dependencies>
</project>'''

        self.dependency_template = '''        <dependency>
            <groupId>{group_id}</groupId>
            <artifactId>{artifact_id}</artifactId>
            <version>{version}</version>
{scope}        </dependency>'''

    def extract_dependencies(self, gradle_file_path: str) -> List[Dict[str, str]]:
        """
        Extract dependencies from build.gradle file.
        
        Args:
            gradle_file_path: Path to build.gradle file
            
        Returns:
            List of dictionaries with dependency info
        """
        dependencies = []
        
        try:
            with open(gradle_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {gradle_file_path}: {e}")
            return dependencies

        # Pattern to match dependencies in build.gradle
        # Matches: implementation 'groupId:artifactId:version'
        # Also matches: testImplementation, runtimeOnly, compileOnly, etc.
        patterns = [
            r"implementation\s+['\"]([^'\"]+)['\"]",
            r"testImplementation\s+['\"]([^'\"]+)['\"]",
            r"runtimeOnly\s+['\"]([^'\"]+)['\"]",
            r"compileOnly\s+['\"]([^'\"]+)['\"]",
        ]

        # Track which dependencies we've seen
        seen = set()

        for pattern_idx, pattern in enumerate(patterns):
            matches = re.finditer(pattern, content)
            
            for match in matches:
                dep_string = match.group(1)
                
                # Skip if already added
                if dep_string in seen:
                    continue
                seen.add(dep_string)

                # Parse: groupId:artifactId:version
                parts = dep_string.split(':')
                if len(parts) >= 3:
                    dependency = {
                        'groupId': parts[0],
                        'artifactId': parts[1],
                        'version': parts[2],
                        'scope': 'test' if 'testImplementation' in pattern else 'compile'
                    }
                    dependencies.append(dependency)

        return dependencies

    def generate_dependency_xml(self, dependency: Dict[str, str]) -> str:
        """
        Generate XML for a single dependency.
        
        Args:
            dependency: Dictionary with groupId, artifactId, version, scope
            
        Returns:
            XML string for the dependency
        """
        scope_str = f'<scope>{dependency["scope"]}</scope>\n            ' if dependency.get('scope') != 'compile' else ''
        
        return self.dependency_template.format(
            group_id=dependency['groupId'],
            artifact_id=dependency['artifactId'],
            version=dependency['version'],
            scope=scope_str
        )

    def generate_pom_xml(self, gradle_file_path: str, dependencies: List[Dict[str, str]]) -> str:
        """
        Generate complete pom.xml content.
        
        Args:
            gradle_file_path: Path to build.gradle (for extracting project name)
            dependencies: List of dependencies
            
        Returns:
            Complete pom.xml XML string
        """
        # Extract project name from directory
        project_dir = os.path.dirname(gradle_file_path)
        project_name = os.path.basename(project_dir) or 'gradle-app'
        
        # Sanitize project name for Maven
        artifact_id = re.sub(r'[^a-zA-Z0-9\-_]', '-', project_name.lower())
        group_id = 'com.example'

        # Generate dependencies XML
        dependencies_xml = ''
        if dependencies:
            dep_xmls = [self.generate_dependency_xml(dep) for dep in dependencies]
            dependencies_xml = '\n\n'.join(dep_xmls)
        else:
            dependencies_xml = '        <!-- No dependencies found -->'

        # Generate POM
        pom_content = self.pom_template.format(
            group_id=group_id,
            artifact_id=artifact_id,
            version='1.0.0',
            project_name=project_name,
            dependencies=dependencies_xml
        )

        return pom_content

    def convert_file(self, gradle_file_path: str) -> Tuple[bool, str]:
        """
        Convert a single build.gradle file to pom.xml.
        
        Args:
            gradle_file_path: Path to build.gradle file
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        gradle_file_path = os.path.abspath(gradle_file_path)
        
        # Check if file exists
        if not os.path.isfile(gradle_file_path):
            return False, f"File not found: {gradle_file_path}"

        # Check if it's actually a build.gradle file
        if not gradle_file_path.endswith('build.gradle'):
            return False, f"Not a build.gradle file: {gradle_file_path}"

        # Extract dependencies
        dependencies = self.extract_dependencies(gradle_file_path)

        # Generate POM content
        pom_content = self.generate_pom_xml(gradle_file_path, dependencies)

        # Write pom.xml in same directory as build.gradle
        pom_file_path = os.path.join(os.path.dirname(gradle_file_path), 'pom.xml')

        try:
            with open(pom_file_path, 'w', encoding='utf-8') as f:
                f.write(pom_content)
            return True, f"Created: {pom_file_path} ({len(dependencies)} dependencies)"
        except Exception as e:
            return False, f"Error writing {pom_file_path}: {e}"

    def convert_directory(self, root_path: str, recursive: bool = True) -> Dict[str, any]:
        """
        Convert all build.gradle files in a directory.
        
        Args:
            root_path: Root directory to search
            recursive: Whether to search subdirectories
            
        Returns:
            Dictionary with conversion results
        """
        root_path = os.path.abspath(root_path)

        # Check if path exists
        if not os.path.isdir(root_path):
            print(f"Error: Directory not found: {root_path}")
            return {'success': False, 'results': []}

        print(f"\n{'='*70}")
        print(f"Gradle to Maven POM Converter")
        print(f"{'='*70}")
        print(f"Scanning directory: {root_path}")
        print(f"Recursive: {recursive}")
        print(f"{'='*70}\n")

        results = {
            'success': True,
            'root_path': root_path,
            'total_files': 0,
            'successful': 0,
            'failed': 0,
            'results': []
        }

        # Find all build.gradle files
        if recursive:
            gradle_files = []
            for root, dirs, files in os.walk(root_path):
                for file in files:
                    if file == 'build.gradle':
                        gradle_files.append(os.path.join(root, file))
        else:
            gradle_files = [os.path.join(root_path, 'build.gradle')] if os.path.isfile(os.path.join(root_path, 'build.gradle')) else []

        results['total_files'] = len(gradle_files)

        if not gradle_files:
            print("No build.gradle files found!")
            print(f"Searched in: {root_path}")
            return results

        print(f"Found {len(gradle_files)} build.gradle file(s):\n")

        # Convert each file
        for gradle_file in gradle_files:
            success, message = self.convert_file(gradle_file)
            
            status = "✅" if success else "❌"
            print(f"{status} {message}")

            results['results'].append({
                'gradle_file': gradle_file,
                'success': success,
                'message': message
            })

            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1

        # Print summary
        print(f"\n{'='*70}")
        print(f"CONVERSION SUMMARY")
        print(f"{'='*70}")
        print(f"Total files found:     {results['total_files']}")
        print(f"Successfully converted: {results['successful']} ✅")
        print(f"Failed:                {results['failed']} ❌")
        print(f"{'='*70}\n")

        return results


def print_usage():
    """Print usage information."""
    print("""
Usage:
    python gradle_to_pom_converter.py <path_to_folder>
    python gradle_to_pom_converter.py .
    python gradle_to_pom_converter.py c:\\path\\to\\projects

Options:
    -h, --help      Show this help message
    -s, --single    Only scan current directory (non-recursive)
    -v, --verbose   Print detailed information

Examples:
    # Convert all build.gradle files in current directory and subdirectories
    python gradle_to_pom_converter.py .

    # Convert all build.gradle files in a specific directory
    python gradle_to_pom_converter.py c:\\Users\\uday\\Desktop\\test

    # Convert only in current directory (not subdirectories)
    python gradle_to_pom_converter.py . -s

What it does:
    1. Finds all build.gradle files in the specified directory
    2. Extracts dependencies from each build.gradle
    3. Converts them to Maven format
    4. Creates pom.xml in the same directory as build.gradle

Output:
    - pom.xml files created next to each build.gradle
    - Console output showing success/failure for each file
    - Summary report at the end
    """)


def main():
    """Main entry point."""
    # Parse arguments
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        sys.exit(0)

    target_path = sys.argv[1]
    recursive = True
    verbose = False

    # Check for additional flags
    if len(sys.argv) > 2:
        if '-s' in sys.argv or '--single' in sys.argv:
            recursive = False
        if '-v' in sys.argv or '--verbose' in sys.argv:
            verbose = True

    # Create converter
    converter = GradleToPomConverter()

    # Convert directory
    results = converter.convert_directory(target_path, recursive=recursive)

    # Exit with appropriate code
    sys.exit(0 if results['success'] and results['failed'] == 0 else 1)


if __name__ == '__main__':
    main()
