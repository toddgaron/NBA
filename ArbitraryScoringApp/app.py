from flask import Flask, render_template, request, redirect
from requests import get
from simplejson import loads
from pandas import DataFrame,to_datetime

from dateutil.relativedelta import *
from asteval import Interpreter

app = Flask(__name__)
app.vars={}
aeval = Interpreter()

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=='GET':
		return render_template('stockinfo.html')
	else:
		app.vars['Name']=request.form['name']
		print app.vars
		try:
			w =  map(lambda x: aeval(str(x).join(app.vars['Name'].split('%'))), range(100))
			print w
			if None in w or len(filter(lambda x: x < 0, w)) !=0:
				return render_template('errorpage.html')
			return render_template('outpage.html', name=w)
		except:
			return render_template('errorpage.html')

if __name__ == '__main__':
  app.run(port=33507)
