import re
from ast_node import Node

def tokenize(rule_str):
    return re.findall(r'\(|\)|AND|OR|\w+\s*(?:>=|>|<=|<|==)\s*(?:\d+|\'[^\']+\')', rule_str)

def parse_condition(condition_str):
    match = re.match(r"(\w+)\s*(>=|>|<=|<|==)\s*(\d+|'[^']+')", condition_str.strip())
    if match:
        attribute, operator, value = match.groups()
        return Node("operand", (attribute, operator, value))
    raise ValueError(f"Invalid format: {condition_str}")

def parse_expression(tokens):
    def parse():
        nonlocal tokens
        if not tokens:
            return None

        left = parse_condition(tokens.pop(0)) if tokens[0] not in ['(', 'AND', 'OR'] else None

        while tokens:
            if tokens[0] == '(':
                tokens.pop(0)  # Remove opening parenthesis
                left = parse()
                if tokens and tokens[0] == ')':
                    tokens.pop(0)  # Remove closing parenthesis
            elif tokens[0] in ['AND', 'OR']:
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

def evaluate_node(node,user_data):
    if node.node_type =="operand":
        attribute,operator,value=node.value
        user_value=user_data.get(attribute)

        if operator ==">":
            return user_value > int(value)
        elif operator == ">=":
            return user_value >= int(value)
        elif operator == "<":
            return user_value < int(value)
        elif operator =="<=":
            return user_value <= int(value)
        elif operator == "==":
            value =value.strip("'")
            return user_value==value
        else:
            raise ValueError(f"Unsupported operator: {operator}")
    elif node.node_type=="operator":
        left_res=evaluate_node(node.left,user_data)
        right_res=evaluate_node(node.right,user_data)

        if node.value=="AND":
            return left_res and right_res
        else:
            return left_res or right_res

def combine_rules(rules):
    # Initialize an empty list to store the parsed ASTs for each rule
    ast_list = []
    
    # Parse each rule into an AST and add it to the list
    for rule in rules:
        ast = create_rule(rule)  # Assuming create_rule is already implemented
        ast_list.append(ast)
    
    # If there is only one rule, no need to combine, return its AST
    if len(ast_list) == 1:
        return ast_list[0]
    
    # Initialize the root of the combined AST as an OR operator node
    combined_ast = {
        "type": "operator",
        "value": "OR",
        "left": None,
        "right": None
    }
    
    # Start with the first AST in the list
    current_ast = ast_list[0]
    
    # Combine all subsequent ASTs using the OR operator
    for next_ast in ast_list[1:]:
        combined_ast = {
            "type": "operator",
            "value": "OR",
            "left": current_ast,
            "right": next_ast
        }
        current_ast = combined_ast  # Update the current_ast to the combined result

    return combined_ast
'''def test_rule_evaluation():
    rule_str = "age > 30 AND department == 'Sales'"
    user_data = {"age": 35, "department": "Sales"}

    # Step 1: Parse the rule into an AST
    ast = parse_rule(rule_str)
    print("AST Representation:", ast)

    # Step 2: Evaluate the rule against user data
    result = evaluate_node(ast, user_data)
    print("Evaluation Result:", result)  # Should print True or False based on the rule

# Running the test
if __name__ == "__main__":
    test_rule_evaluation()
rule_str = "age > 30 AND department == 'Sales'"
ast = parse_rule(rule_str)
print(ast)'''
