"""Maintain Claude's copies of the three shared teaching skills using stdlib only."""

import argparse
from pathlib import Path


SKILLS = ("cf-explain-finance", "cf-notebook-help", "cf-revision-quiz")
ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report differences without writing files")
    args = parser.parse_args()
    sources = {}
    for name in SKILLS:
        source = ROOT / ".agents" / "skills" / name / "SKILL.md"
        if not source.is_file():
            parser.error(f"Missing canonical skill: {source.relative_to(ROOT)}")
        sources[name] = source.read_text(encoding="utf-8")

    mismatches = []
    for name, content in sources.items():
        target = ROOT / ".claude" / "skills" / name / "SKILL.md"
        if target.is_file() and target.read_text(encoding="utf-8") == content:
            continue
        mismatches.append(name)
        if not args.check:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8", newline="\n")

    if args.check and mismatches:
        print("Skill copies need updating: " + ", ".join(mismatches))
        print("Run: uv run --no-sync python .utilities/sync_skills.py")
        return 1
    print(f"Teaching skills {'checked' if args.check else 'synchronised'}: {len(SKILLS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
