#!/usr/bin/env python3
"""
Decision Linter - Validates decision records against Thresh standards.

Comprehensive validation of decision record markdown files including:
- Frontmatter YAML parsing and schema validation
- Required fields and format checks
- decision_id format validation (DEC-YYYYMMDD-NNN)
- Body structure validation (decision statement, alternatives, rationale, etc.)
- Jira issue key format validation in source references
- Impact scope and confidence tracking

Decision records are stored in: product/context/decisions/

Usage:
  lint_decision.py <file.md>                     # Validate single decision
  lint_decision.py decisions/                    # Validate directory
  lint_decision.py --report decisions/ > report.txt # Generate text report

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
from datetime import datetime


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


class DecisionLinter:
    """Validates decision records against Thresh standards."""

    # Required frontmatter fields
    REQUIRED_FIELDS = {
        'decision_id': 'Decision identifier (DEC-YYYYMMDD-NNN format)',
        'date': 'Decision date (ISO 8601 format)',
        'source': 'Source reference (Jira issue or context)',
        'decision_statement': 'Clear statement of the decision made',
        'impact_scope': 'Scope of impact (which stories/epics affected)',
        'decided_by': 'Person or role that made the decision',
        'confidence': 'Confidence level in the decision',
        'status': 'Decision status (Active, Superseded, Revoked)',
    }

    # Valid decision status values
    VALID_STATUSES = ['Active', 'Superseded', 'Revoked']

    # Valid confidence levels
    VALID_CONFIDENCE = ['High', 'Medium', 'Low']

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
        """Lint a single decision file. Returns True if valid (no errors)."""
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
        """Extract and parse YAML frontmatter from decision file."""
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

        # Validate decision_id format: DEC-YYYYMMDD-NNN
        if 'decision_id' in fm:
            decision_id = str(fm['decision_id']).strip()
            if not re.match(r'^DEC-\d{8}-\d{3}$', decision_id):
                self._add_error('decision_id',
                    f"Invalid format: '{decision_id}' (use DEC-YYYYMMDD-NNN, e.g., DEC-20240206-001)")
            else:
                # Validate that date in ID is valid ISO date
                date_part = decision_id[4:12]
                try:
                    datetime.strptime(date_part, '%Y%m%d')
                except ValueError:
                    self._add_error('decision_id',
                        f"Invalid date in decision_id: {date_part} (must be valid YYYYMMDD)")

        # Validate date field (ISO 8601)
        if 'date' in fm and fm['date']:
            date_val = str(fm['date']).strip()
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_val):
                self._add_error('date',
                    f"Invalid date format: '{date_val}' (use YYYY-MM-DD)")
            else:
                # Try to parse to ensure it's a valid date
                try:
                    datetime.strptime(date_val, '%Y-%m-%d')
                except ValueError:
                    self._add_error('date',
                        f"Invalid date value: '{date_val}' (not a real date)")

        # Validate confidence level
        if 'confidence' in fm:
            confidence = fm['confidence']
            if confidence not in self.VALID_CONFIDENCE:
                self._add_error('confidence',
                    f"Invalid confidence: '{confidence}' (use: {', '.join(self.VALID_CONFIDENCE)})")

        # Validate status
        if 'status' in fm:
            status = fm['status']
            if status not in self.VALID_STATUSES:
                self._add_error('status',
                    f"Invalid status: '{status}' (use: {', '.join(self.VALID_STATUSES)})")

        # Validate source reference (should be Jira format: PROJECT-NNN)
        if 'source' in fm:
            source = str(fm['source']).strip()
            # Check if it looks like a Jira issue key
            if not re.match(r'^[A-Z]+-\d+$', source):
                self._add_warn('source',
                    f"Source '{source}' doesn't match Jira issue format (PROJECT-NNN)")

        # Validate impact_scope (should reference stories/epics)
        if 'impact_scope' in fm:
            scope = fm['impact_scope']
            if isinstance(scope, str):
                scope_str = scope.strip()
                if not scope_str:
                    self._add_error('impact_scope', "Impact scope cannot be empty")
                # Check if it references any stories (STORY-XXX-XX or similar patterns)
                elif not any(pattern in scope_str for pattern in ['STORY-', 'EPIC-', 'CHAR', 'epic']):
                    self._add_warn('impact_scope',
                        "Impact scope should reference affected stories or epics")
            elif isinstance(scope, list):
                if not scope:
                    self._add_error('impact_scope', "Impact scope list cannot be empty")
            else:
                self._add_error('impact_scope', "Impact scope must be string or list")

        # Validate decided_by (person or role name)
        if 'decided_by' in fm:
            decided_by = str(fm['decided_by']).strip()
            if len(decided_by) < 3:
                self._add_warn('decided_by',
                    f"Decided by value seems too short: '{decided_by}'")

    def _validate_body(self):
        """Validate decision body content."""
        body = self.body
        if not body.strip():
            self._add_error(None, "Decision body is empty (add content after frontmatter)")
            return

        # Check for required sections
        required_sections = {
            '## Decision Statement': 'Clear statement of the decision',
            '## Alternatives Considered': 'Discussion of other options evaluated',
            '## Rationale': 'Reasoning behind the decision',
            '## Impact Scope': 'Which stories, epics, or systems are affected',
        }

        for section, description in required_sections.items():
            if section not in body:
                self._add_error(None,
                    f"Missing '{section}' section ({description})")

        # Check for optional but recommended sections
        recommended_sections = {
            '## Timeline': 'When will this decision be implemented',
            '## Reversibility': 'How easily can this decision be reversed',
            '## Dependencies': 'What this decision depends on',
        }

        for section, description in recommended_sections.items():
            if section not in body:
                self._add_warn(None,
                    f"Missing '{section}' section (recommended: {description})")

        # Check content length
        content_length = len(body.strip())
        if content_length < 300:
            self._add_warn(None,
                f"Decision record is quite brief ({content_length} characters, recommend 300+)")
        elif content_length > 8000:
            self._add_warn(None,
                f"Decision record is very long ({content_length} characters, consider breaking down)")

        # Check for decision_statement field expanded in body
        if self.frontmatter and 'decision_statement' in self.frontmatter:
            stmt = self.frontmatter['decision_statement']
            if isinstance(stmt, str) and len(stmt) < 10:
                self._add_warn(None,
                    f"Decision statement in frontmatter is brief ({len(stmt)} chars), elaborate in body")

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
        """Check if decision passed validation (no errors)."""
        return self.error_count == 0


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: lint_decision.py <file.md> | <directory/> | --report <directory/>")
        print()
        print("Examples:")
        print("  python lint_decision.py decisions/DEC-20240206-001.md")
        print("  python lint_decision.py product/context/decisions/")
        print("  python lint_decision.py --report decisions/ > report.txt")
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
        linter = DecisionLinter()
        is_valid = linter.lint_file(str(filepath))

        if is_valid:
            passed_files += 1

        results.append((filepath, linter))

    # Output results
    if generate_report:
        print("# Decision Record Validation Report\n")
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
