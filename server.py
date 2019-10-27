from flask import Flask, render_template, jsonify, request
import couchdb

app = Flask(__name__)
couch = couchdb.Server()
db = couch['transactions']

def query(mango):
  response = {}
  for row in db.find(mango):
    response.update({ row['_id']: row })
  return {"response": response}

@app.route('/')
def main():
  return render_template('index.html', data=get_transactions())

@app.route('/api/transaction/<limit>', methods=['GET'])
def get_transactions_with_limit(limit):
  mango = {
    "selector": {
      "_id": {"$gt": 0}
    },
    "limit": limit
  }
  return query(mango)

@app.route('/api/transaction/', methods=['GET', 'POST'])
def get_transactions():
  if request.method == 'GET':
    return get_transactions_with_limit(25)
  if request.method == 'DELETE':
    return None

@app.route('/api/transaction/<id>', methods=['GET', 'DELETE', 'PUT'])
def get_transaction_by_id(id):
  if request.method == 'GET':
    mango = {
      "selector": {
        "_id": id
      }
    }
    return query(mango)
  if request.method == 'DELETE':
    return None
  if request.method == 'POST':
    return None

if __name__ == '__main__':
  app.run(debug=True)