from flask import Flask, render_template, request, redirect
from requests import get
from simplejson import loads
from pandas import DataFrame,to_datetime
from bokeh.plotting import figure
from bokeh.embed import components
from dateutil.relativedelta import *

app = Flask(__name__)
app.vars={}

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
	if request.method=='GET':
		return render_template('stockinfo.html')
	else:
		app.vars['Name']=request.form['name']
		app.vars['Method']=request.form['method']
		try:
			w=get('https://www.quandl.com/api/v3/datasets/WIKI/{}/data.json?api_key=2HugxxJfTx-g-EXLbDx-'.format(app.vars['Name'])).text
			w=loads(w)
			w=DataFrame([row[1:] for row in w['dataset_data']['data']],columns=w['dataset_data']['column_names'][1:],index=to_datetime([row[0] for row in w['dataset_data']['data']]))
			first = w.index[0]
			print first
			last = first +relativedelta(months=-1)
			print last
			wMonth=w[first:last]
			p=figure(width=800,height=400,x_axis_type="datetime")
			p.line(wMonth.index,list(w[app.vars['Method']]))
			p.xaxis.axis_label = "Time"
			p.yaxis.axis_label = app.vars['Method']
			script, div = components(p)
			return render_template('outpage.html',name=app.vars['Name'],s=script,d=div)
		except:
			return render_template('errorpage.html')

if __name__ == '__main__':
  app.run(port=33507)
