#!/usr/bin/env python3
"""Local validator for the OpenCode Expert Skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

DEFAULT_SKILL_DIR = Path(__file__).resolve().parent.parent

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
FRONTMATTER_DELIM = "---"
REQUIRED_FRONTMATTER_KEYS = ("name", "description")
OPTIONAL_FRONTMATTER_KEYS = ("license", "compatibility", "metadata")
MAX_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
DESCRIPTION_MIN_LENGTH = 1
REQUIRED_FILES = (
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "sources/official-documentation.md",
    "sources/source-code-map.md",
    "sources/source-manifest.json",
    "sources/version-history.md",
)
REQUIRED_SOURCE_KEYS = ("topic", "source_type", "source_url", "verification_status")
EVIDENCE_LEVELS = ("DOCUMENTED", "SOURCE VERIFIED", "PARTIAL", "UNVERIFIED")
MERMAID_KEYWORDS = (
    "flowchart",
    "sequenceDiagram",
    "stateDiagram",
    "classDiagram",
    "erDiagram",
    "gantt",
    "pie",
    "graph",
)

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*$", re.DOTALL)
LINK_RE = re.compile(r"\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s[^)]*)?\)")
REFERENCE_LINK_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(\S+)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
FENCE_RE = re.compile(r"^(\s*)```(\w*)\s*$")


@dataclass
class Finding:
    severity: str
    check: str
    message: str
    path: str = ""
    line: Optional[int] = None

    def as_dict(self):
        return {
            "severity": self.severity,
            "check": self.check,
            "message": self.message,
            "path": self.path,
            "line": self.line,
        }


def _parse_frontmatter(text):
    lines = text.splitlines()
    if len(lines) < 2 or lines[0].strip() != FRONTMATTER_DELIM:
        return {}, "missing_frontmatter_delimiter"
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == FRONTMATTER_DELIM:
            end_index = idx
            break
    if end_index is None:
        return {}, "unterminated_frontmatter"
    body = "\n".join(lines[1:end_index])
    fields = {}
    for raw_line in body.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        fields[key] = value
    return fields, None


def _slugify(heading):
    slug = heading.strip().lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = slug.strip().lower()
    slug = re.sub(r"[\s]+", "-", slug)
    return slug


def check_frontmatter(skill_dir, findings):
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8")
    fields, err = _parse_frontmatter(text)
    if err:
        findings.append(Finding("ERROR", "frontmatter", "SKILL.md " + err, str(skill_file)))
        return
    unknown = sorted(set(fields) - set(REQUIRED_FRONTMATTER_KEYS) - set(OPTIONAL_FRONTMATTER_KEYS))
    for key in unknown:
        findings.append(Finding("INFO", "frontmatter", "Unknown frontmatter field ignored by spec: " + key, str(skill_file)))
    for key in REQUIRED_FRONTMATTER_KEYS:
        if key not in fields or fields[key].strip() == "":
            findings.append(Finding("ERROR", "frontmatter", "Required frontmatter field missing: " + key, str(skill_file)))
    name = fields.get("name", "").strip()
    description = fields.get("description", "").strip()
    if "name" in fields and fields["name"].strip() != "":
        if not NAME_RE.match(name):
            findings.append(Finding("ERROR", "frontmatter", "Invalid skill name: " + name, str(skill_file)))
        if not (1 <= len(name) <= MAX_NAME_LENGTH):
            findings.append(Finding("ERROR", "frontmatter", "Skill name length out of range (1-64): " + str(len(name)), str(skill_file)))
        # Official Agent Skills install layout often uses skills/<name>/.
        # Repository clones may use any directory name (e.g. opencode-expert-skill).
        # Only enforce name==folder when nested under a "skills" parent directory.
        skill_dir_name = skill_dir.resolve().name
        parent_name = skill_dir.resolve().parent.name
        if name != skill_dir_name:
            if parent_name.lower() == "skills":
                findings.append(
                    Finding(
                        "ERROR",
                        "frontmatter",
                        "Skill name '" + name + "' does not match directory name '" + skill_dir_name + "' under skills/",
                        str(skill_dir / "SKILL.md"),
                    )
                )
            else:
                findings.append(
                    Finding(
                        "INFO",
                        "frontmatter",
                        "Skill name '" + name + "' differs from repository directory '" + skill_dir_name + "' (allowed outside skills/ install layout)",
                        str(skill_dir / "SKILL.md"),
                    )
                )
    if "description" in fields and fields["description"].strip() != "":
        if not (DESCRIPTION_MIN_LENGTH <= len(description) <= MAX_DESCRIPTION_LENGTH):
            findings.append(Finding("ERROR", "frontmatter", "Description length out of range (1-%d): %d" % (MAX_DESCRIPTION_LENGTH, len(description)), str(skill_file)))
    if "license" in fields and fields["license"].strip() == "":
        findings.append(Finding("WARNING", "frontmatter", "Optional field 'license' present but empty", str(skill_file)))
    if "compatibility" in fields and fields["compatibility"].strip() == "":
        findings.append(Finding("WARNING", "frontmatter", "Optional field 'compatibility' present but empty", str(skill_file)))
    if "metadata" in fields:
        meta = fields["metadata"]
        if not isinstance(meta, dict):
            findings.append(Finding("WARNING", "frontmatter", "Optional field 'metadata' should be a string-to-string map", str(skill_file)))


def check_required_files(skill_dir, findings):
    for rel in REQUIRED_FILES:
        p = skill_dir / rel
        if not p.is_file():
            findings.append(Finding("ERROR", "required_files", "Missing required file: " + rel, str(p)))
            continue
        if p.stat().st_size <= 0:
            findings.append(Finding("ERROR", "required_files", "Required file is empty: " + rel, str(p)))
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        found = sorted(p.name for p in refs_dir.glob("*.md") if re.match(r"^\d{2}-.*\.md$", p.name))
        if not found:
            findings.append(Finding("ERROR", "required_references", "No required reference modules found in references/", str(refs_dir)))
    else:
        findings.append(Finding("ERROR", "required_references", "Missing references directory", str(refs_dir)))


def check_source_manifest(skill_dir, findings):
    p = skill_dir / "sources/source-manifest.json"
    if not p.is_file():
        findings.append(Finding("ERROR", "source_manifest", "Missing source manifest: " + str(p), str(p)))
        return
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append(Finding("ERROR", "source_manifest", "source-manifest.json is not valid JSON: " + str(exc), str(p)))
        return
    if not isinstance(data, list):
        findings.append(Finding("ERROR", "source_manifest", "source-manifest.json must be a JSON array", str(p)))
        return
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            findings.append(Finding("ERROR", "source_manifest", "source-manifest.json entry " + str(i) + " is not an object", str(p)))
            continue
        for key in REQUIRED_SOURCE_KEYS:
            if key not in entry or not isinstance(entry.get(key), str) or entry.get(key, "").strip() == "":
                findings.append(Finding("ERROR", "source_manifest", "source-manifest.json entry " + str(i) + " missing required key: " + key, str(p)))
        url = entry.get("source_url", "")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            findings.append(Finding("ERROR", "source_manifest", "source-manifest.json entry " + str(i) + " has invalid source_url: " + str(url), str(p)))
        status = entry.get("verification_status", "")
        if status and status not in EVIDENCE_LEVELS:
            findings.append(Finding("WARNING", "source_manifest", "source-manifest.json entry " + str(i) + " has unknown verification_status: " + str(status), str(p)))


def check_file_links(skill_dir, findings):
    for md_file in sorted(p for p in skill_dir.rglob("*.md") if p.is_file()):
        text = md_file.read_text(encoding="utf-8")
        rel = md_file.relative_to(skill_dir).as_posix()
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if re.match(r"^[a-z]+://", target, re.IGNORECASE) or target.startswith("mailto:") or target.startswith("#"):
                continue
            path_part = target.split("#", 1)[0]
            if path_part == "":
                continue
            resolved = (md_file.parent / path_part).resolve()
            if not resolved.exists():
                findings.append(Finding("ERROR", "links", "Broken markdown link target: " + target + " (from " + rel + ")", str(md_file)))
        headings = set()
        for line in text.splitlines():
            hm = HEADING_RE.match(line)
            if hm:
                headings.add(_slugify(hm.group(2)))
        for m in REFERENCE_LINK_RE.finditer(text):
            target = m.group(1).strip()
            if re.match(r"^[a-z]+://", target, re.IGNORECASE) or target.startswith("mailto:") or target.startswith("#") or target == "":
                continue
            path_part = target.split("#", 1)[0]
            if path_part == "":
                continue
            resolved = (md_file.parent / path_part).resolve()
            if not resolved.exists():
                findings.append(Finding("ERROR", "links", "Broken reference-style link target: " + target + " (from " + rel + ")", str(md_file)))
        for m in LINK_RE.finditer(text):
            target = m.group(1).strip()
            if not target.startswith("#"):
                continue
            slug = _slugify(target[1:])
            if slug not in headings:
                findings.append(Finding("WARNING", "links", "Broken same-file anchor: " + target + " (in " + rel + ")", str(md_file)))


def check_mermaid(skill_dir, findings):
    for md_file in sorted(p for p in skill_dir.rglob("*.md") if p.is_file()):
        lines = md_file.read_text(encoding="utf-8").splitlines()
        in_fence = False
        fence_lang = ""
        block_lines = []
        blocks = []
        for line in lines:
            fm = FENCE_RE.match(line)
            if fm:
                if not in_fence:
                    in_fence = True
                    fence_lang = (fm.group(2) or "").strip().lower()
                    block_lines = []
                else:
                    blocks.append((fence_lang, block_lines))
                    in_fence = False
                    fence_lang = ""
                    block_lines = []
            elif in_fence:
                block_lines.append(line)
        if in_fence:
            findings.append(Finding("ERROR", "mermaid", "Unbalanced code fence at end of file", str(md_file)))
        for lang, block in blocks:
            if lang == "mermaid" or lang.startswith("mermaid"):
                joined = "\n".join(block)
                if not any(kw.lower() in joined.lower() for kw in MERMAID_KEYWORDS):
                    findings.append(Finding("WARNING", "mermaid", "Mermaid block without recognized diagram keyword", str(md_file)))


def run_checks(skill_dir):
    findings = []
    check_frontmatter(skill_dir, findings)
    check_required_files(skill_dir, findings)
    check_source_manifest(skill_dir, findings)
    check_file_links(skill_dir, findings)
    check_mermaid(skill_dir, findings)
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate the OpenCode Expert Skill.")
    parser.add_argument("--skill-dir", type=str, default=str(DEFAULT_SKILL_DIR), help="Path to the skill directory")
    args = parser.parse_args(argv)
    skill_dir = Path(args.skill_dir).resolve()
    findings = run_checks(skill_dir)
    errors = [f for f in findings if f.severity == "ERROR"]
    warnings = [f for f in findings if f.severity == "WARNING"]
    infos = [f for f in findings if f.severity == "INFO"]
    print("OpenCode Expert Skill validation")
    print("Skill directory: " + str(skill_dir))
    print("ERRORS: " + str(len(errors)) + "  WARNINGS: " + str(len(warnings)) + "  INFO: " + str(len(infos)))
    for f in errors:
        print("[ERROR] " + f.check + ": " + f.message + " (" + str(f.path) + ")")
    for f in warnings:
        print("[WARNING] " + f.check + ": " + f.message + " (" + str(f.path) + ")")
    for f in infos:
        print("[INFO] " + f.check + ": " + f.message + " (" + str(f.path) + ")")
    if errors:
        print("RESULT: FAIL")
        return 1
    print("RESULT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())