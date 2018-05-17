from flask import Flask, request, url_for, redirect, send_from_directory, json
from model.employee import Employee
from flask_mysqldb import MySQL


app = Flask(__name__, static_url_path='')

didLogin = False



@app.route('/<path:path>')
def send_html(path):
    send_from_directory('Hello/static',path)

@app.route('/login', methods = ['POST'])
def login():
    name = request.form['nm']
    pwd = request.form['pwd']
    return redirect(url_for('user_validation', name=name, pwd=pwd))

@app.route('/insert', methods=['POST'])
def insert_emp():
    if not didLogin :
        return redirect(url_for('reponse_json', msg='Session invalid'))

    name = request.get_json()['name']
    designation = request.get_json()['designation']
    cur, con = getMysqlConnection()
    cur.execute("INSERT INTO employees (name, designation) VALUES ('" + name + "', '" + designation + "')")

    return request.json

@app.route('/employees')
def employees():
    # db = getMysqlConnection()
    # cur = db['cursor']
    cur, con = getMysqlConnection()
    cur.execute('SELECT * FROM employees limit 100')
    row_headers = [x[0] for x in cur.description]
    rv = cur.fetchall()
    json_data = []
    for result in rv:
        json_data.append(dict(zip(row_headers, result)))
    return json.dumps(json_data)

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

def getMysqlConnection():
    mysql = MySQL(app)
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '123456'
    app.config['MYSQL_DB'] = 'ema'
    app.config['MYSQL_HOST'] = 'localhost'
    mysql.init_app(app)

    connection = mysql.connect
    cursor = connection.cursor()
    return cursor, connection
#{"cursor":cursor,"connection":connection}




if __name__ == '__main__':
    app.debug = True
    app.run()
