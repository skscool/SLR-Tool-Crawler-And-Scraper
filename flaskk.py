# from flask import Flask, jsonify, render_template, request
from flask import *
import os

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('landing.html')

@app.route('/receive_data',methods =['POST'])
def fun():
	# print("sdfadsf = ",request.form['input_data'])
	file = open("temp.txt","w")
	file.write(request.form['input_data'])
	return redirect('/download')

@app.route('/download')
def downloadFile ():
    path = os.getcwd()+"/temp.txt"
    print("Sending file...")
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
	app.run(port = 8888, debug = True)
