from flask import Flask, request, jsonify
from rule_parser import parse_rule

app = Flask(__name__)

def node_to_json(node):
    """Convert Node object to JSON serializable dictionary."""
    if node.node_type == "operand":
        return {
            "type": "operand",
            "value": list(node.value)  # Convert to list for the output
        }
    elif node.node_type == "operator":
        result = {
            "type": "operator",
            "value": node.value,
        }
        if node.left:
            result["left"] = node_to_json(node.left)
        if node.right:
            result["right"] = node_to_json(node.right)
        return result

@app.route('/create_rule', methods=['POST'])
def create_rule():
    rule_str = request.json.get('rule')
    try:
        ast = parse_rule(rule_str)
        ast_json = node_to_json(ast)  # Convert Node to JSON serializable structure
        return jsonify({"ast": ast_json})
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
            value = value.strip("'")  # If value is wrapped in quotes (for strings)
            return user_value == value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    elif node['node_type'] == "operator":
        left_res = evaluate_node(node['left'], user_data)
        right_res = evaluate_node(node['right'], user_data)

        # Perform logical operation (AND/OR)
        if node['value'] == "AND":
            return left_res and right_res
        else:  # For OR
            return left_res or right_res
    else:
        raise ValueError("Unsupported node type")


# API endpoint to evaluate rules
@app.route('/evaluate_node', methods=['POST'])
def evaluate_node_api():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract the 'node' (AST) and 'user_data'
        node = data.get('node')
        user_data = data.get('user_data')

        # Validate inputs
        if not node or not user_data:
            return jsonify({"error": "Invalid input. Please provide both 'node' and 'user_data'."}), 400

        # Call evaluate_node function
        result = evaluate_node(node, user_data)

        # Return the result as JSON
        return jsonify({"result": result}), 200

    except Exception as e:
        # Handle any errors and return as JSON response
        return jsonify({"error": str(e)}), 500

@app.route('/combine_rules', methods=['POST'])
def combine_rules():
    data = request.json
    rules = data.get('rules', [])
    
    if not rules:
        return jsonify({"error": "No rules provided"}), 400
    
    try:
        combined_ast = combine_rules(rules)
        return jsonify({"combined_ast": combined_ast}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)