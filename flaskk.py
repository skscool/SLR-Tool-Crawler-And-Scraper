# from flask import Flask, jsonify, render_template, request
from flask import *
app = Flask(__name__)

@app.route('/')
def home():
	return render_template('landing.html')

@app.route('/receive_data',methods =['POST'])
def fun():
	print("sdfadsf = ",request.form['input_data'])
	return redirect('/')

if __name__ == '__main__':
	app.run(port = 8888, debug = True)