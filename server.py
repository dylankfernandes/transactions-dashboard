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

@app.route('/api/transaction/<limit>')
def get_transactions_with_limit(limit):
  mango = {
    "selector": {
      "_id": {"$gt": 0}
    },
    "limit": limit
  }
  return query(mango)

@app.route('/api/transaction/')
def get_transactions():
  return get_transactions_with_limit(1000)

@app.route('/api/transaction/<id>')
def get_transaction_by_id(id):
    mango = {
      "selector": {
        "_id": id
      }
    }
    return query(mango)

if __name__ == '__main__':
  app.run(debug=True)