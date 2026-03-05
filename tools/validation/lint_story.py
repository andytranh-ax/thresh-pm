#!/usr/bin/env python3
"""
Story Linter - Validates user stories against Thresh standards.

Comprehensive validation of story markdown files including:
- Frontmatter YAML parsing and schema validation
- Required fields and format checks
- Body structure validation (User Story, Acceptance Criteria, Edge Cases, etc.)
- Acceptance criteria GIVEN/WHEN/THEN format validation
- Figma reference validation
- Tag vocabulary validation
- Points estimation (fibonacci scale)

Usage:
  lint_story.py <file.md>                     # Validate single story
  lint_story.py stories/                      # Validate directory
  lint_story.py --report stories/ > report.md # Generate HTML-style report

Exit codes:
  0 = All files passed (no errors)
  1 = One or more files have errors
"""

import sys
import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class MessageLevel(Enum):
    """Message severity levels."""
    ERROR = "ERROR"
    WARN = "WARN"
    INFO = "INFO"


@dataclass
class Message:
    """Validation message."""
    level: MessageLevel
    text: str
    field: Optional[str] = None


class StoryLinter:
    """Validates stories against Thresh standards with color output."""

    # Required frontmatter fields
    REQUIRED_FIELDS = {
        'story_id': 'Story identifier (e.g., STORY-123-45 or UX-456)',
        'title': 'Descriptive story title',
        'epic': 'Parent epic name',
        'status': 'Workflow status',
        'points': 'Fibonacci story points estimate',
        'tags': 'Array of domain tags',
        'figma_ref': 'Figma design URL',
        'ux_id': 'UX identifier (if design-related)',
        'category': 'Category (Frontend, Backend, Full-stack, Design, Data)',
    }

    # Valid story statuses
    VALID_STATUSES = ['Draft', 'Ready', 'In Progress', 'In Review', 'Done']

    # Valid points values (planning poker / fibonacci)
    VALID_POINTS = [1, 2, 3, 5, 8, 13]

    # Valid story categories
    VALID_CATEGORIES = ['Frontend', 'Backend', 'Full-stack', 'Design', 'Data']

    # Valid domain tags (from tag_vocabulary.md)
    VALID_TAGS = {
        # Feature domains
        'ui', 'api', 'backend', 'frontend', 'design', 'ux', 'data',
        'infrastructure', 'auth', 'payments', 'mobile', 'web',
        'performance', 'security', 'testing', 'documentation',
        # Story status/type
        'feature', 'bugfix', 'refactor', 'chore', 'spike', 'tech-debt',
        # Priority
        'critical', 'high', 'medium', 'low',
        # Teams/Review
        'design-review', 'architecture-review', 'legal-review',
        'platform-team', 'mobile-team', 'payments-team', 'vendor-dependency',
        # Complexity
        'complex', 'simple', 'investigation',
        # Cross-cutting
        'accessibility', 'internationalization', 'compliance',
        'contract-change', 'breaking-change'
    }

    # ANSI color codes
    COLOR_ERROR = '\033[91m'    # Bright red
    COLOR_WARN = '\033[93m'     # Bright yellow
    COLOR_INFO = '\033[94m'     # Bright blue
    COLOR_SUCCESS = '\033[92m'  # Bright green
    COLOR_RESET = '\033[0m'

    def __init__(self):
        self.messages: List[Message] = []
        self.frontmatter: Optional[Dict] = None
        self.body: str = ""

    def lint_file(self, filepath: str) -> bool:
        """Lint a single story file. Returns True if valid (no errors)."""
        self.messages = []
        self.frontmatter = None
        self.body = ""

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            self._add_error(None, f"File not found: {filepath}")
            return False
        except Exception as e:
            self._add_error(None, f"Error reading file: {e}")
            return False

        # Parse frontmatter
        self.frontmatter, self.body = self._parse_frontmatter(content)

        if self.frontmatter is None:
            self._add_error(None, "Invalid or missing YAML frontmatter (must be between --- delimiters)")
            return False

        # Validate frontmatter
        self._validate_frontmatter()

        # Validate body structure
        self._validate_body()

        return self.error_count == 0

    def _parse_frontmatter(self, content: str) -> Tuple[Optional[Dict], str]:
        """Extract and parse YAML frontmatter from story file."""
        lines = content.split('\n')

        if not lines or lines[0].strip() != '---':
            return None, ""

        # Find closing delimiter
        end_idx = -1
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                end_idx = i
                break

        if end_idx == -1:
            self._add_error(None, "Frontmatter not properly closed (missing closing ---)")
            return None, ""

        # Parse YAML
        yaml_content = '\n'.join(lines[1:end_idx])
        try:
            frontmatter = yaml.safe_load(yaml_content)
            if not isinstance(frontmatter, dict):
                self._add_error(None, "Frontmatter must be valid YAML key-value pairs")
                return None, ""
            body = '\n'.join(lines[end_idx+1:])
            return frontmatter, body
        except yaml.YAMLError as e:
            self._add_error(None, f"Invalid YAML in frontmatter: {e}")
            return None, ""

    def _validate_frontmatter(self):
        """Validate all frontmatter fields against schema."""
        fm = self.frontmatter
        if not fm:
            return

        # Check required fields
        for field in self.REQUIRED_FIELDS.keys():
            if field not in fm:
                self._add_error(field, f"Missing required field: {field}")
            elif fm[field] is None or (isinstance(fm[field], str) and not fm[field].strip()):
                self._add_error(field, f"Field cannot be empty: {field}")

        # Validate story_id format: STORY-XXX-XX or UX-XXX
        if 'story_id' in fm:
            story_id = str(fm['story_id']).strip()
            if not re.match(r'^(STORY-\d{3}-\d{2}|UX-\d{3})$', story_id):
                self._add_error('story_id',
                    f"Invalid format: '{story_id}' (use STORY-XXX-XX or UX-XXX)")

        # Validate title
        if 'title' in fm:
            title = str(fm['title']).strip()
            words = len(title.split())
            if words > 10:
                self._add_warn('title', f"Title too long ({words} words, recommend <10)")
            if words < 3:
                self._add_warn('title', f"Title too short ({words} words, recommend 3-10)")

        # Validate status (case-sensitive)
        if 'status' in fm:
            status = fm['status']
            if status not in self.VALID_STATUSES:
                self._add_error('status',
                    f"Invalid status: '{status}' (use: {', '.join(self.VALID_STATUSES)})")

        # Validate points (fibonacci scale)
        if 'points' in fm:
            try:
                points = int(fm['points'])
                if points not in self.VALID_POINTS:
                    self._add_error('points',
                        f"Invalid points: {points} (use fibonacci: 1, 2, 3, 5, 8, 13)")
            except (ValueError, TypeError):
                self._add_error('points', f"Points must be an integer, got: {fm['points']}")

        # Validate tags (required, non-empty list, all from vocabulary)
        if 'tags' in fm:
            tags = fm['tags']
            if not isinstance(tags, list):
                self._add_error('tags', f"Tags must be a YAML list, got: {type(tags).__name__}")
            elif len(tags) == 0:
                self._add_error('tags', "At least one tag required")
            else:
                # Check for domain tag (first tag should be a domain)
                domain_tags = {'ui', 'api', 'backend', 'frontend', 'design', 'ux', 'data',
                             'infrastructure', 'auth', 'payments', 'mobile', 'web',
                             'performance', 'security', 'testing', 'documentation'}
                has_domain = any(t in domain_tags for t in tags)
                if not has_domain:
                    self._add_warn('tags',
                        "At least one domain tag required (ui, api, backend, frontend, etc.)")

                for tag in tags:
                    if tag not in self.VALID_TAGS:
                        self._add_warn('tags', f"Unknown tag: '{tag}' (not in vocabulary)")

        # Validate category
        if 'category' in fm:
            category = fm['category']
            if category not in self.VALID_CATEGORIES:
                self._add_error('category',
                    f"Invalid category: '{category}' (use: {', '.join(self.VALID_CATEGORIES)})")

            # Check Figma ref for Frontend category
            if category == 'Frontend' and 'figma_ref' not in fm:
                self._add_error('figma_ref',
                    "Frontend stories MUST have a figma_ref")

        # Validate Figma reference URL
        if 'figma_ref' in fm:
            figma_ref = str(fm['figma_ref']).strip()
            if not (figma_ref.startswith('https://www.figma.com') or figma_ref.startswith('https://figma.com')):
                self._add_error('figma_ref',
                    "Figma URL must start with https://figma.com or https://www.figma.com")
            if 'node-id=' not in figma_ref:
                self._add_error('figma_ref',
                    "Figma URL must include node-id parameter (e.g., ?node-id=123:456)")

        # Validate UX ID format if present
        if 'ux_id' in fm and fm['ux_id']:
            ux_id = str(fm['ux_id']).strip()
            if not re.match(r'^UX-\d{3,4}$', ux_id):
                self._add_warn('ux_id', f"UX ID format should be UX-XXX or UX-XXXX, got: {ux_id}")

        # Validate date fields (ISO 8601)
        for date_field in ['created', 'updated']:
            if date_field in fm and fm[date_field]:
                date_val = str(fm[date_field]).strip()
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
                    self._add_error(date_field,
                        f"Invalid date format: '{date_val}' (use YYYY-MM-DD)")

    def _validate_body(self):
        """Validate story body structure and content."""
        body = self.body
        if not body.strip():
            self._add_error(None, "Story body is empty (add content after frontmatter)")
            return

        # Check for User Story section
        if '## User Story' not in body:
            self._add_error(None, "Missing '## User Story' section")

        # Check for Acceptance Criteria section
        if '## Acceptance Criteria' not in body:
            self._add_error(None, "Missing '## Acceptance Criteria' section")
        else:
            self._validate_acceptance_criteria(body)

        # Check for Edge Cases section (WARN if missing)
        if '## Edge Cases' not in body:
            self._add_warn(None, "Missing '## Edge Cases' section (should include empty, error, loading states)")
        else:
            self._validate_edge_cases(body)

        # Check for Components Used section
        if '## Components Used' not in body:
            self._add_warn(None, "Missing '## Components Used' section")
        else:
            self._validate_components(body)

        # Check for Dependencies section
        if '## Dependencies' not in body:
            self._add_error(None, "Missing '## Dependencies' section")

    def _validate_acceptance_criteria(self, body: str):
        """Validate acceptance criteria format (GIVEN/WHEN/THEN)."""
        # Extract acceptance criteria section
        match = re.search(r'##+ Acceptance Criteria(.+?)(?=##|$)', body, re.DOTALL)
        if not match:
            self._add_error(None, "Acceptance Criteria section not properly formatted")
            return

        ac_text = match.group(1)

        # Must use GIVEN/WHEN/THEN format
        given_count = ac_text.count('GIVEN')
        when_count = ac_text.count('WHEN')
        then_count = ac_text.count('THEN')

        if given_count == 0 or when_count == 0 or then_count == 0:
            self._add_error(None,
                "Acceptance criteria must use GIVEN/WHEN/THEN format")

        # Check for minimum 2 acceptance criteria (GIVEN blocks)
        if given_count < 2:
            self._add_error(None,
                f"Minimum 2 acceptance criteria required, found {given_count}")

        # Warn if too many
        if given_count > 8:
            self._add_warn(None,
                f"High number of acceptance criteria ({given_count}, consider 2-5)")

        # Check for vague language
        vague_words = ['should', 'might', 'hopefully', 'probably', 'maybe', 'could', 'perhaps']
        vague_found = []
        for word in vague_words:
            if re.search(rf'\b{word}\b', ac_text, re.IGNORECASE):
                vague_found.append(word)

        if vague_found:
            self._add_warn(None,
                f"Vague language in acceptance criteria: {', '.join(vague_found)}")

    def _validate_edge_cases(self, body: str):
        """Validate edge cases section covers required scenarios."""
        match = re.search(r'##+ Edge Cases(.+?)(?=##|$)', body, re.DOTALL)
        if not match:
            return

        edge_cases_text = match.group(1).lower()

        required_cases = {
            'empty': 'empty state',
            'error': 'error state',
            'loading': 'loading state'
        }

        missing = []
        for key, label in required_cases.items():
            if key not in edge_cases_text:
                missing.append(label)

        if missing:
            self._add_warn(None,
                f"Edge cases should include: {', '.join(missing)}")

    def _validate_components(self, body: str):
        """Check Components Used section."""
        match = re.search(r'##+ Components Used(.+?)(?=##|$)', body, re.DOTALL)
        if not match:
            return

        components_text = match.group(1).strip()
        if not components_text or components_text in ['', '\n']:
            self._add_warn(None, "Components Used section is empty")

    def _add_error(self, field: Optional[str], text: str):
        """Add error message."""
        self.messages.append(Message(MessageLevel.ERROR, text, field))

    def _add_warn(self, field: Optional[str], text: str):
        """Add warning message."""
        self.messages.append(Message(MessageLevel.WARN, text, field))

    def _add_info(self, field: Optional[str], text: str):
        """Add info message."""
        self.messages.append(Message(MessageLevel.INFO, text, field))

    @property
    def error_count(self) -> int:
        """Count of error messages."""
        return sum(1 for m in self.messages if m.level == MessageLevel.ERROR)

    @property
    def warn_count(self) -> int:
        """Count of warning messages."""
        return sum(1 for m in self.messages if m.level == MessageLevel.WARN)

    @property
    def info_count(self) -> int:
        """Count of info messages."""
        return sum(1 for m in self.messages if m.level == MessageLevel.INFO)

    def report(self, use_color: bool = True) -> str:
        """Generate formatted validation report."""
        if not self.messages:
            prefix = f"{self.COLOR_SUCCESS}✓{self.COLOR_RESET}" if use_color else "✓"
            return f"{prefix} PASSED: No issues found"

        output = []

        # Group by level
        errors = [m for m in self.messages if m.level == MessageLevel.ERROR]
        warns = [m for m in self.messages if m.level == MessageLevel.WARN]
        infos = [m for m in self.messages if m.level == MessageLevel.INFO]

        if errors:
            prefix = f"{self.COLOR_ERROR}✗ ERRORS{self.COLOR_RESET}" if use_color else "✗ ERRORS"
            output.append(prefix)
            for msg in errors:
                output.append(f"  - {msg.text}")

        if warns:
            prefix = f"{self.COLOR_WARN}⚠ WARNINGS{self.COLOR_RESET}" if use_color else "⚠ WARNINGS"
            output.append(prefix)
            for msg in warns:
                output.append(f"  - {msg.text}")

        if infos:
            prefix = f"{self.COLOR_INFO}ℹ INFO{self.COLOR_RESET}" if use_color else "ℹ INFO"
            output.append(prefix)
            for msg in infos:
                output.append(f"  - {msg.text}")

        return '\n'.join(output)

    def is_valid(self) -> bool:
        """Check if story passed validation (no errors)."""
        return self.error_count == 0


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: lint_story.py <file.md> | <directory/> | --report <directory/>")
        print()
        print("Examples:")
        print("  python lint_story.py stories/STORY-100-01.md")
        print("  python lint_story.py stories/")
        print("  python lint_story.py --report stories/ > report.txt")
        sys.exit(0)

    path_arg = sys.argv[1]
    generate_report = '--report' in sys.argv

    if generate_report:
        path_arg = sys.argv[2] if len(sys.argv) > 2 else '.'

    path = Path(path_arg)

    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)

    # Find all markdown files
    if path.is_file():
        files = [path]
    else:
        files = sorted(path.glob('**/*.md'))
        files = [f for f in files if not f.name.startswith('.')]

    if not files:
        print(f"No markdown files found in {path}")
        sys.exit(0)

    # Lint all files
    results = []
    total_files = 0
    passed_files = 0

    for filepath in files:
        total_files += 1
        linter = StoryLinter()
        is_valid = linter.lint_file(str(filepath))

        if is_valid:
            passed_files += 1

        results.append((filepath, linter))

    # Output results
    if generate_report:
        print("# Story Validation Report\n")
        print(f"Generated: {total_files} files validated\n")

        for filepath, linter in results:
            status = "PASS" if linter.is_valid() else "FAIL"
            print(f"## {filepath.name} [{status}]")
            print(f"Path: `{filepath}`\n")
            print(linter.report(use_color=False))
            print()
    else:
        for filepath, linter in results:
            status = "✓" if linter.is_valid() else "✗"
            print(f"{status} {filepath.name}")
            report = linter.report(use_color=True)
            for line in report.split('\n'):
                print(f"    {line}")

    # Summary
    print()
    print(f"{'='*70}")
    print(f"SUMMARY: {passed_files}/{total_files} files passed validation")
    print(f"{'='*70}")

    if passed_files < total_files:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
