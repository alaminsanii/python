from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>Calculator API</h2>
    <p><a href='/calc/10/5/add'>Add</a></p>
    <p><a href='/calc/10/5/sub'>Subtract</a></p>
    <p><a href='/calc/10/5/mul'>Multiply</a></p>
    <p><a href='/calc/10/5/div'>Divide</a></p>
    """

@app.route("/calc/<int:a>/<int:b>/<op>")
def calculate(a, b, op):

    if op == "add":
        result = a + b

    elif op == "sub":
        result = a - b

    elif op == "mul":
        result = a * b

    elif op == "div":
        result = a / b if b != 0 else "Cannot divide by zero"

    else:
        result = "Invalid operation"

    return jsonify({
        "a": a,
        "b": b,
        "operation": op,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)