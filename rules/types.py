from dataclasses import dataclass

@dataclass
class RuleType:
    """Base class for different types of rules."""
    rule_name: str
    message: str
    severity: int 
    # 1: informational/positive, 
    # 2: minor issue 
    # 3: moderate issue 
    # 4: major issue 
    # 5: critical issue - heavily affected the game
