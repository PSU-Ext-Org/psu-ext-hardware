#!/usr/bin/env python3
"""Maintain the repository's DEP5 copyright and licence metadata.

DEP5 is Debian's machine-readable copyright format.  This repository adds two
DEP5-compatible extra fields to each ``Files`` stanza:

* ``X-PSU-EXT-Section`` groups blocks by licence; and
* ``X-PSU-EXT-Block`` names the specific set of files that share metadata.

Run this script from the repository root:

    python LICENSES/dep5.py list
    python LICENSES/dep5.py validate
    python LICENSES/dep5.py add --section cern-ohl-s-2.0 \
        --block original-source manufacturing/new-file.csv

Use ``create-section`` only for a new licence section.  It deliberately does
not modify existing copyright, licence, or comment metadata.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


# The script lives in ``LICENSES/``; its parent is always the repository root.
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DEP5_PATH = REPOSITORY_ROOT / "LICENSES" / "dep5"
SECTION_FIELD = "X-PSU-EXT-Section"
BLOCK_FIELD = "X-PSU-EXT-Block"
REQUIRED_FILE_FIELDS = {"Files", "Copyright", "License", SECTION_FIELD, BLOCK_FIELD}
FIELD_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]*$")


@dataclass
class Stanza:
    """One blank-line-separated Debian-control-file stanza.

    A list, rather than a dictionary, preserves the original field order when
    the file is rewritten.  DEP5 comments can be multiline, so values retain
    their continuation lines separated by ``\n``.
    """

    fields: list[tuple[str, str]]

    def get(self, name: str) -> str | None:
        """Return a field value, or ``None`` when the field is absent."""
        return next((value for key, value in self.fields if key == name), None)

    def set(self, name: str, value: str) -> None:
        """Replace a field without changing its position, or append it."""
        for index, (key, _) in enumerate(self.fields):
            if key == name:
                self.fields[index] = (name, value)
                return
        self.fields.append((name, value))


def parse(text: str) -> list[Stanza]:
    """Parse the small Debian-control-file subset used by DEP5.

    Continuation lines start with whitespace and belong to the field directly
    above them.  Invalid field names and orphaned continuation lines are
    rejected so this utility never writes malformed control-file syntax.
    """
    stanzas: list[Stanza] = []
    for raw_stanza in text.strip().split("\n\n"):
        fields: list[tuple[str, str]] = []
        for line in raw_stanza.splitlines():
            if line[:1].isspace():
                if not fields:
                    raise ValueError("continuation line without a field")
                key, value = fields[-1]
                fields[-1] = (key, f"{value}\n{line[1:]}")
            elif ":" in line:
                key, value = line.split(":", 1)
                if not FIELD_NAME.fullmatch(key):
                    raise ValueError(f"invalid DEP5 field name: {key}")
                fields.append((key, value.lstrip()))
            else:
                raise ValueError(f"invalid DEP5 line: {line}")
        stanzas.append(Stanza(fields))
    return stanzas


def render(stanzas: list[Stanza]) -> str:
    """Render stanzas as UTF-8-friendly DEP5 text with LF line endings."""
    rendered: list[str] = []
    for stanza in stanzas:
        lines: list[str] = []
        for key, value in stanza.fields:
            value_lines = value.split("\n")
            # DEP5 permits an empty field followed by continuation lines.  Do
            # not add a trailing space to that empty first line.
            lines.append(f"{key}:" if not value_lines[0] else f"{key}: {value_lines[0]}")
            lines.extend(f" {line}" for line in value_lines[1:])
        rendered.append("\n".join(lines))
    return "\n\n".join(rendered) + "\n"


def load() -> list[Stanza]:
    """Load the authoritative DEP5 file from ``LICENSES/dep5``."""
    return parse(DEP5_PATH.read_text(encoding="utf-8"))


def is_files_stanza(stanza: Stanza) -> bool:
    """Return whether a stanza assigns metadata to one or more files."""
    return stanza.get("Files") is not None


def find_block(stanzas: list[Stanza], section: str, block: str) -> Stanza:
    """Find exactly one named Files block, rejecting ambiguous targets."""
    matches = [
        stanza
        for stanza in stanzas
        if stanza.get(SECTION_FIELD) == section and stanza.get(BLOCK_FIELD) == block
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one block {section}/{block}, found {len(matches)}")
    return matches[0]


def repository_paths(paths: list[str]) -> list[str]:
    """Validate and normalize input files to sorted, POSIX repository paths.

    DEP5 paths are repository-relative.  Resolving first prevents callers from
    accidentally adding a path outside this checkout, while sorting and
    de-duplicating makes repeated ``add`` calls idempotent.
    """
    normalized: list[str] = []
    for argument in paths:
        candidate = (Path.cwd() / argument).resolve()
        try:
            relative = candidate.relative_to(REPOSITORY_ROOT)
        except ValueError as error:
            raise ValueError(f"path is outside the repository: {argument}") from error
        if not candidate.is_file():
            raise ValueError(f"path is not a file: {argument}")
        normalized.append(relative.as_posix())
    return sorted(set(normalized))


def validate(stanzas: list[Stanza]) -> list[str]:
    """Return every detected DEP5 consistency error without modifying files.

    The header must identify DEP5, each Files stanza must be complete and
    uniquely named, explicitly listed files must exist, and each licence used
    by a Files stanza must have a standalone ``License`` stanza.
    """
    errors: list[str] = []
    if not stanzas or stanzas[0].get("Format") != "https://www.debian.org/doc/packaging-manuals/copyright-format/1.0/":
        errors.append("header stanza must contain the DEP5 Format field")

    # A standalone License stanza has no Files field.  Only its first line is
    # its identifier; following continuation lines are the licence text.
    declared_licenses = {
        (stanza.get("License") or "").split("\n", 1)[0]
        for stanza in stanzas[1:]
        if not is_files_stanza(stanza) and stanza.get("License")
    }
    blocks: set[tuple[str, str]] = set()
    for number, stanza in enumerate(stanzas[1:], start=2):
        if not is_files_stanza(stanza):
            continue
        names = [key for key, _ in stanza.fields]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            errors.append(f"stanza {number} repeats fields: {', '.join(duplicates)}")
        missing = REQUIRED_FILE_FIELDS.difference(key for key, _ in stanza.fields)
        if missing:
            errors.append(f"stanza {number} is missing: {', '.join(sorted(missing))}")
            continue
        empty = sorted(field for field in REQUIRED_FILE_FIELDS if not (stanza.get(field) or "").strip())
        if empty:
            errors.append(f"stanza {number} has empty fields: {', '.join(empty)}")
            continue
        identity = (stanza.get(SECTION_FIELD) or "", stanza.get(BLOCK_FIELD) or "")
        if identity in blocks:
            errors.append(f"duplicate block: {identity[0]}/{identity[1]}")
        blocks.add(identity)
        # Wildcard patterns are valid DEP5 paths but cannot be checked as one
        # literal filesystem entry.  Every explicit path must be present.
        for path in (stanza.get("Files") or "").split():
            if "*" not in path and "?" not in path and not (REPOSITORY_ROOT / path).is_file():
                errors.append(f"stanza {number} lists missing file: {path}")
        license_name = (stanza.get("License") or "").split("\n", 1)[0]
        if license_name not in declared_licenses:
            errors.append(f"stanza {number} references undeclared licence: {license_name}")
    return errors


def command_list(_: argparse.Namespace) -> int:
    """Print the recognized section/block inventory without editing DEP5."""
    stanzas = load()
    errors = validate(stanzas)
    if errors:
        raise ValueError("\n".join(errors))
    for stanza in stanzas[1:]:
        if is_files_stanza(stanza):
            print(f"{stanza.get(SECTION_FIELD)}/{stanza.get(BLOCK_FIELD)}: "
                  f"{stanza.get('License')} | {stanza.get('Copyright')} | "
                  f"{len((stanza.get('Files') or '').split())} files")
    return 0


def command_add(args: argparse.Namespace) -> int:
    """Add existing files to an existing block, preserving its legal metadata."""
    stanzas = load()
    errors = validate(stanzas)
    if errors:
        raise ValueError("\n".join(errors))
    stanza = find_block(stanzas, args.section, args.block)
    existing = set((stanza.get("Files") or "").split())
    additions = [path for path in repository_paths(args.paths) if path not in existing]
    if not additions:
        print("No paths added.")
        return 0
    # A continuation line per file keeps long file lists readable in DEP5.
    stanza.set("Files", "\n".join(sorted(existing.union(additions))))
    DEP5_PATH.write_text(render(stanzas), encoding="utf-8", newline="\n")
    print(f"Added {len(additions)} path(s) to {args.section}/{args.block}.")
    return 0


def command_create_section(args: argparse.Namespace) -> int:
    """Append one new section and its first Files block.

    A section is intentionally immutable after creation through this command.
    Add further files with ``add`` so existing legal declarations cannot be
    silently changed by routine maintenance.
    """
    stanzas = load()
    errors = validate(stanzas)
    if errors:
        raise ValueError("\n".join(errors))
    if any(stanza.get(SECTION_FIELD) == args.section for stanza in stanzas if is_files_stanza(stanza)):
        raise ValueError(f"section already exists: {args.section}")
    files = "\n".join(repository_paths(args.paths))
    fields = [
        ("Files", files),
        ("Copyright", args.copyright),
        ("License", args.license),
        (SECTION_FIELD, args.section),
        (BLOCK_FIELD, args.block),
    ]
    if args.comment:
        fields.append(("Comment", args.comment))
    stanzas.append(Stanza(fields))
    DEP5_PATH.write_text(render(stanzas), encoding="utf-8", newline="\n")
    print(f"Created {args.section}/{args.block}.")
    return 0


def command_validate(_: argparse.Namespace) -> int:
    """Exit successfully only when DEP5 passes all local consistency checks."""
    errors = validate(load())
    if errors:
        raise ValueError("\n".join(errors))
    print("DEP5 validation passed.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Manage DEP5 licence sections and blocks.",
        epilog="Run 'list' to view valid --section/--block targets before using 'add'.",
    )
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("list").set_defaults(handler=command_list)
    add = commands.add_parser("add")
    add.add_argument("--section", required=True, help="existing X-PSU-EXT-Section value")
    add.add_argument("--block", required=True, help="existing X-PSU-EXT-Block value")
    add.add_argument("paths", nargs="+", help="existing repository-relative files to add")
    add.set_defaults(handler=command_add)
    create = commands.add_parser("create-section")
    create.add_argument("--section", required=True, help="new X-PSU-EXT-Section value")
    create.add_argument("--block", required=True, help="new X-PSU-EXT-Block value")
    create.add_argument("--copyright", required=True, help="DEP5 Copyright field")
    create.add_argument("--license", required=True, help="DEP5 License identifier")
    create.add_argument("--comment", help="optional DEP5 Comment field")
    create.add_argument("paths", nargs="+", help="existing files for the new block")
    create.set_defaults(handler=command_create_section)
    commands.add_parser("validate").set_defaults(handler=command_validate)
    args = parser.parse_args()
    try:
        return args.handler(args)
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
