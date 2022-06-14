from flask import request, Flask, jsonify, Response

import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname='devpipelineusers' user='andrewfletcher' host='localhost'")
cursor = conn.cursor()


@app.route('/user/add', methods=['POST'])
def add_user():
  form = request.form
  first_name = form.get('first_name')
  if first_name == '':
    return jsonify("First Name Required"), 400

  last_name = form.get('last_name')
  if last_name == '':
    return jsonify("Last Name Required"), 400

  email = form.get('email')
  if email == '':
    return jsonify("Email Required"), 400

  password = form.get('password')
  if password == '':
    return jsonify("Password Required"), 400

  city = form.get('city')
  state = form.get('state')
  active = form.get('active', 'true')

  cursor.execute("INSERT INTO Users (first_name, last_name, email, password, city, state) VALUES (%s, %s, %s, %s, %s, %s)", (first_name, last_name, email, password, city, state))

  return jsonify("User Added"), 200


@app.route('/user/edit/<user_id>', methods=['POST'])
def edit_user(user_id):
  cursor.execute("SELECT user_id, first_name, last_name, email, password, city, state, active FROM Users WHERE user_id = %s", (user_id, ))
  results = cursor.fetchone()

  if results == None:
    return jsonify("Edit Who?"), 404
  else:
    user_form = request.form
    first_name = user_form.get('first_name')
    last_name = user_form.get('last_name')
    email = user_form.get('email')
    password = user_form.get('password')
    city = user_form.get('city')
    state = user_form.get('state')
    active = user_form.get('active')

    if first_name == '':
      first_name = results[1]

    if last_name == '':
      last_name = results[2]

    if email == '':
      email = results[3]

    if password == '':
      password = results[4]

    if city == '':
      city = results[5]

    if state == '':
      state = results[6]

    if active == '':
      active = results[7]

  cursor.execute("UPDATE Users SET first_name = %s, last_name = %s, email = %s, password = %s, city = %s, state = %s, active = %s WHERE user_id = %s", [first_name, last_name, email, password, city, state, active, user_id])

  return jsonify("Edited User"), 200



@app.route('/user/delete/<user_id>', methods=['DELETE'])
def delete_user(user_id):
  cursor.execute("SELECT user_id, first_name, last_name FROM Users WHERE user_id = %s", [user_id, ])
  query_results = cursor.fetchone()

  if query_results == None:
    return jsonify("Temporarily Out of Coffee"), 503
  else:
    cursor.execute("DELETE FROM Users WHERE user_id = %s", [user_id,])

    return jsonify("Record Deleted"), 200


@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
  cursor.execute("SELECT user_id, first_name, last_name, email, password, city, state, active FROM Users WHERE user_id = %s", [user_id, ])
  results = cursor.fetchone()

  if results == None:
    return jsonify("Server Refuses to Brew Coffee because it is, Permanently, a Teapot"), 418
  else: 
    result_dictionary = {
      'user_id': results[0],
      'first_name': results[1],
      'last_name': results[2],
      'email': results[3],
      'password': results[4],
      'city': results[5],
      'state': results[6],
      'active': results[7]
    }

    return jsonify(result_dictionary), 200


@app.route('/users', methods=['GET'])
def get_all_users():
  cursor.execute("SELECT user_id, first_name, last_name, email, password, city, state, active  FROM Users")
  results = cursor.fetchall()

  list_of_users = []

  if results == []:
    return jsonify("No Users Found"), 404
  else:
    for user in results:
      list_of_users.append({
        'user_id': user[0],
        'first_name': user[1],
        'last_name': user[2],
        'email': user[3],
        'password': user[4],
        'city': user[5],
        'state': user[6],
        'active': user[7]
      })

    output_dictionary = {
      "users": list_of_users
    }

    return jsonify(output_dictionary), 200


if __name__ == '__main__':
  app.run()