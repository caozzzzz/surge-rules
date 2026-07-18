from pathlib import Path
import ipaddress
import sys


RULE_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
    "IP-ASN",
    "GEOIP",
    "PROCESS-NAME",
    "USER-AGENT",
    "URL-REGEX",
    "DEST-PORT",
    "PROTOCOL",
}

LOGICAL_TYPES = {"AND", "OR", "NOT"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue

        parts = [item.strip() for item in line.split(",")]
        if len(parts) < 2:
            errors.append(f"{path}:{number}: incomplete rule: {line}")
            continue

        rule_type = parts[0].upper()
        if rule_type in LOGICAL_TYPES:
            # Logical rules contain nested comma-separated sub-rules, so the
            # ordinary field-count/policy check does not apply to them.
            continue

        if rule_type not in RULE_TYPES:
            errors.append(f"{path}:{number}: unsupported rule type: {rule_type}")
            continue

        # External rulesets must not contain a policy. Most ordinary rules have
        # two fields; IP rules may have the third field `no-resolve`.
        if len(parts) > 3 or (len(parts) == 3 and parts[2] != "no-resolve"):
            errors.append(f"{path}:{number}: possible embedded policy: {line}")

        if rule_type in {"IP-CIDR", "IP-CIDR6"}:
            try:
                ipaddress.ip_network(parts[1], strict=False)
            except ValueError as exc:
                errors.append(f"{path}:{number}: invalid CIDR ({exc}): {line}")

    return errors


def main() -> int:
    files = sorted(Path("rules").glob("*.list"))
    if not files:
        print("No rule files found", file=sys.stderr)
        return 1

    errors = [error for path in files for error in validate(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Validated {len(files)} Surge rule files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
from pathlib import Path
import ipaddress
import sys


RULE_TYPES = {
    "DOMAIN",
    "DOMAIN-SUFFIX",
    "DOMAIN-KEYWORD",
    "IP-CIDR",
    "IP-CIDR6",
    "IP-ASN",
    "GEOIP",
    "PROCESS-NAME",
    "USER-AGENT",
    "URL-REGEX",
    "DEST-PORT",
    "PROTOCOL",
}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    for number, raw in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue

        parts = [item.strip() for item in line.split(",")]
        if len(parts) < 2:
            errors.append(f"{path}:{number}: incomplete rule: {line}")
            continue

        rule_type = parts[0].upper()
        if rule_type not in RULE_TYPES:
            errors.append(f"{path}:{number}: unsupported rule type: {rule_type}")
            continue

        # External rulesets must not contain a policy. Most ordinary rules have
        # two fields; IP rules may have the third field `no-resolve`.
        if len(parts) > 3 or (len(parts) == 3 and parts[2] != "no-resolve"):
            errors.append(f"{path}:{number}: possible embedded policy: {line}")

        if rule_type in {"IP-CIDR", "IP-CIDR6"}:
            try:
                ipaddress.ip_network(parts[1], strict=False)
            except ValueError as exc:
                errors.append(f"{path}:{number}: invalid CIDR ({exc}): {line}")

    return errors


def main() -> int:
    files = sorted(Path("rules").glob("*.list"))
    if not files:
        print("No rule files found", file=sys.stderr)
        return 1

    errors = [error for path in files for error in validate(path)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print(f"Validated {len(files)} Surge rule files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

