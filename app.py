from flask import Flask, request, url_for, redirect, send_from_directory, json


app = Flask(__name__, static_url_path='')
app.debug = True


employees = []
didLogin = False

@app.route('/<path:path>')
def send_html(path):
    send_from_directory('Hello/static',path)


@app.route('/success/<name>/<pwd>')
def user_validation(name, pwd):
    if name == 'admin' and pwd == 'password':
        global didLogin
        didLogin = True
        return redirect(url_for('reponse_json', msg='Login successful'))
    else:
        return redirect(url_for('reponse_json', msg='Invalid credentials'))


@app.route('/reponse/<msg>')
def reponse_json(msg):
    return json.dumps({'success': True, 'message': msg}), 200, {
        'ContentType': 'application/json'}


@app.route('/login', methods = ['POST'])
def login():
    name = request.form['nm']
    pwd = request.form['pwd']
    return redirect(url_for('user_validation', name=name, pwd=pwd))

@app.route('/insert', methods=['POST'])
def insert_emp():
    if not didLogin :
        return redirect(url_for('reponse_json', msg='Invalid credentials'))

    return request.get_json()
    # return name + ' has been added to list'


if __name__ == '__main__':
    app.run(debug=True)
