import re
from ast_node import Node

def tokenize(rule_str):
    return re.findall(r'\(|\)|AND|OR|\w+\s*(?:>=|>|<=|<|==)\s*(?:\d+|\'[^\']+\')', rule_str)

def parse_condition(condition_str):
    match = re.match(r"(\w+)\s*(>=|>|<=|<|==)\s*(\d+|\'[^\']+\')", condition_str.strip())
    if match:
        attribute, operator, value = match.groups()
        return Node("operand", (attribute, operator, value))
    raise ValueError(f"Invalid condition format: {condition_str}")

def parse_expression(tokens):
    def parse():
        nonlocal tokens
        if not tokens:
            return None

        left = None

        if tokens[0] == '(':
            tokens.pop(0)  # Remove '('
            left = parse()
            if tokens[0] == ')':
                tokens.pop(0)  # Remove ')'
        else:
            left = parse_condition(tokens.pop(0))

        while tokens:
            if tokens[0] in ['AND', 'OR']:
                op = tokens.pop(0)
                right = parse()
                left = Node("operator", op, left, right)
            else:
                break

        return left

    return parse()

def parse_rule(rule_str):
    tokens = tokenize(rule_str)
    return parse_expression(tokens)

def evaluate_node(node, user_data):
    if node.node_type == "operand":
        attribute, operator, value = node.value
        user_value = user_data.get(attribute)

        if operator == ">":
            return user_value > int(value)
        elif operator == ">=":
            return user_value >= int(value)
        elif operator == "<":
            return user_value < int(value)
        elif operator == "<=":
            return user_value <= int(value)
        elif operator == "==":
            value = value.strip("'")
            return user_value == value
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    
    elif node.node_type == "operator":
        left_res = evaluate_node(node.left, user_data)
        right_res = evaluate_node(node.right, user_data)

        if node.value == "AND":
            return left_res and right_res
        elif node.value == "OR":
            return left_res or right_res
        else:
            raise ValueError(f"Unsupported logical operator: {node.value}")

# For testing purposes, you could define a separate function here
def test_rule_evaluation():
    rule_str = "age > 30 AND department == 'Sales'"
    user_data = {"age": 35, "department": "Sales"}

    ast = parse_rule(rule_str)
    print("AST Representation:", ast)

    result = evaluate_node(ast, user_data)
    print("Evaluation Result:", result)
from ast_node import Node
from rule_parser import parse_rule

def combine_rules(rules):
    """Combine multiple rules into a single AST using OR."""
    if not rules:
        raise ValueError("No rules provided for combination.")

    # Parse each rule into an AST
    ast_list = [parse_rule(rule) for rule in rules]
    
    # If there's only one rule, return its AST
    if len(ast_list) == 1:
        return ast_list[0]

    # Combine the ASTs using the OR operator
    combined_ast = ast_list[0]
    for next_ast in ast_list[1:]:
        combined_ast = Node("operator", "OR", combined_ast, next_ast)

    return combined_ast

if __name__ == "__main__":
    test_rule_evaluation()
