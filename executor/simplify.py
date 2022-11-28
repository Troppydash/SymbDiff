from executor.rule import Rule, RuleApplier
from executor.rules.diff import diffrules
from executor.rules.simple import EvaluateRule, simplerules
from symbols import Expression, literal


def simplify_expression(expression: Expression, rules: list[Rule] | None = None) -> Expression:
    if rules is None:
        rules = []

    applied_rules = [
        *simplerules,
        *diffrules,
        *rules
    ]

    rule_applier = RuleApplier(applied_rules)
    return rule_applier.apply(expression)[1]
