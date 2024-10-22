from flask import Flask, request, jsonify
from rule_parser import parse_rule, combine_rules
from ast_node import Node

app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_str = request.data.decode('utf-8')  # Get the rule as a string
    try:
        ast = parse_rule(rule_str)
        # Return only the root node of the AST
        ast_json = {'type': ast.node_type, 'value': ast.value}
        return jsonify({"ast": ast_json})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    rules = request.json.get('rules')  # Get the list of rules
    if not rules:
        return jsonify({"error": "No rules provided"}), 400
    
    try:
        combined_ast = combine_rules(rules)
        # Return the combined AST as JSON
        return jsonify({"combined_ast": {'type': combined_ast.node_type, 'value': combined_ast.value}})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

def evaluate_node(node, user_data):
    if node['node_type'] == "operand":
        attribute, operator, value = node['value']
        user_value = user_data.get(attribute)

        # Perform comparison based on the operator
        if operator == ">":
            return user_value > int(value)
        elif operator == ">=":
            return user_value >= int(value)
        elif operator == "<":
            return user_value < int(value)
        elif operator == "<=":
            return user_value <= int(value)
        elif operator == "==":
            value = value.strip("'")  # Remove quotes from strings
            return user_value == value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    elif node['node_type'] == "operator":
        left_res = evaluate_node(node['left'], user_data)
        right_res = evaluate_node(node['right'], user_data)

        if node['value'] == "AND":
            return left_res and right_res
        elif node['value'] == "OR":
            return left_res or right_res
        else:
            raise ValueError(f"Unsupported operator in node: {node['value']}")

if __name__ == '__main__':
    app.run(debug=True)
