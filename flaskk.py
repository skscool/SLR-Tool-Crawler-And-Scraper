# from flask import Flask, jsonify, render_template, request
from flask import *
import os
from main import *

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('landing.html')

@app.route('/ACM')
def acm():
	return render_template('ACM.html')

@app.route('/Springer')
def springer():
	return render_template('Springer.html')

@app.route('/IEEE')
def IEEE():
	return render_template('IEEE.html')

@app.route('/ScienceDirect')
def ScienceDirect():
	return render_template('ScienceDirect.html')

@app.route('/receive_data',methods =['POST'])
def fun():
	print("from receive data", request.form)
	# print("sdfadsf = ",request.form['yearStart'])
	getJSON(request.form.to_dict())
	# file = open("temp.txt","w")
	# file.write(request.form['input_data'])
	return redirect('/')

@app.route('/download')
def downloadFile ():
    path = os.getcwd()+"/temp.txt"
    print("Sending file...")
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
	app.run(port = 8888, debug = True)
