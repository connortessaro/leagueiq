from rules.types import RuleType


def build_match_report(rules: list[RuleType], isWin: bool) -> str:
    """
    Builds a human-readable CLI report from rule results.
    This function does not compute logic — it only formats output.
    """

    if not rules:
        return "No major issues detected in this match."

    # sort rules by severity (highest impact first)
    rules_sorted = rules
    if isWin:
        rules_sorted = [rule for rule in rules_sorted if rule.severity >= 3]
    rules_sorted = sorted(rules_sorted, key=lambda r: r.severity, reverse=True)

    sections = {
        "Early Game": [],
        "Economy": [],
        "Objectives": [],
        "Combat": [],
        "Vision": [],
        "Other": [],
    }

    for rule in rules_sorted:
        category = categorize_rule(rule.rule_name)
        sections[category].append(rule)

    report_lines: list[str] = []

    report_lines.append("=== Match Autopsy Report ===\n")
    if isWin:
        report_lines.append("Match Result: Victory\n")
    else:
        report_lines.append("Match Result: Defeat\n")

    for section, rules_in_section in sections.items():
        if not rules_in_section:
            continue

        report_lines.append(f"{section}")
        report_lines.append("-" * len(section))

        for rule in rules_in_section:
            report_lines.append(format_rule(rule))

        report_lines.append("")

    overall = overall_severity(rules_sorted)
    report_lines.append(f"Overall Impact Level: {overall}")

    return "\n".join(report_lines)


def format_rule(rule: RuleType) -> str:
    """
    Formats a single rule into a CLI-friendly bullet point.
    """
    return f"• {rule.message} (severity {rule.severity})"


def categorize_rule(rule_name: str) -> str:
    """
    Simple rule categorization based on naming.
    Keeps report readable without tight coupling.
    """

    name = rule_name.lower()

    if "early" in name or "cs" in name or "xp" in name:
        return "Early Game"
    if "gold" in name or "income" in name:
        return "Economy"
    if "dragon" in name or "baron" in name or "herald" in name or "structure" in name:
        return "Objectives"
    if "damage" in name or "kill" in name:
        return "Combat"
    if "vision" in name:
        return "Vision"

    return "Other"


def overall_severity(rules: list[RuleType]) -> str:
    """
    Computes a simple overall match impact level.
    """

    if not rules:
        return "None"

    max_severity = max(rule.severity for rule in rules)

    if max_severity >= 5:
        return "Critical"
    if max_severity >= 4:
        return "High"
    if max_severity >= 3:
        return "Moderate"
    if max_severity >= 2:
        return "Low"

    return "Minimal"
