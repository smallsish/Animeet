"""
Main.py file that defines the GraphQL endpoints and
initialises them.
"""
from flask import Flask, request, jsonify
from ariadne import graphql_sync
# from ariadne.constants import PLAYGROUND_HTML
from flask_cors import CORS
from .schema import schema

app = Flask(__name__)

CORS(app)


@app.route("/health", methods=["GET"])
def health_check():
    """
    Check whether the service is healthy and running.
    """
    return jsonify({"status": "healthy"}), 200


# @app.route("/graphql", methods=["GET"])
# def graphql_playground():
#     """
#     Allow for the user to send queries and mutations
#     through the GraphQL Playground.
#     """
#     return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    """
    Define the GraphQL endpoint. This is where the
    queries will be redirected to.
    """
    data = request.get_json()

    # Check if data is provided, return 400 if not
    if data is None:
        return jsonify({"error": "No data provided"}), 400

    # Execute the GraphQL query with Ariadne
    success, result = graphql_sync(schema, data, context_value=request, debug=True)  # noqa: E501

    # Return the result and the appropriate HTTP status code
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
