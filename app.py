from flask import Flask, request
import json

app = Flask(__name__)

with open('schemes.json') as f:
    schemes = json.load(f)

@app.route('/')
def home():
    return '''
    <h2>Government Scheme Bot</h2>
    <form method="post" action="/result">
        Category: <input name="type"><br><br>
        Income: <input name="income"><br><br>
        <button type="submit">Find</button>
    </form>
    '''

@app.route('/result', methods=['POST'])
def result():
    user_type = request.form['type']
    income = int(request.form['income'])

    result = []

    for s in schemes:
        if s["category"] == user_type and income <= s["income_limit"]:
            result.append(s["name"])

    if result:
        return "<br>".join(result)
    else:
        return "No scheme found"

app.run(debug=True)