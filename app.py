from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

#create db models (db table)
class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(200), nullable=False)
	#completed = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<Task %r>' % self.id  #returns the id of the task evertime a task is created

#App routes
@app.route('/', methods=['POST','GET'])
def index():

	if request.method == 'POST':
		task_content = request.form['content'] #gets the data from the element with id='content' from the form
		new_task = Todo(content=task_content) #create an object of the model for the data

		#put the data into the database
		try:
			db.session.add(new_task)
			db.session.commit()
			return redirect('/')  #reidrect back to the main page
		except:
			return "Error adding entry"

	else:
		tasks = Todo.query.order_by(Todo.date_created).all()
		return render_template('index.html', tasks= tasks)

@app.route('/delete/<int:id>')
def delete(id):
	task_to_delete = Todo.query.get_or_404(id) #returns the row or 404

	try:
		db.session.delete(task_to_delete)
		db.session.commit()
		return redirect('/')
	except:
		return "Error deleting the entry"

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
	task_to_update = Todo.query.get_or_404(id)

	if request.method == 'POST':
		task_to_update.content = request.form['content']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return "Error updating the record"
	else:
		return render_template('update.html', task=task_to_update)



if __name__ == "__main__":
	app.run(debug=True)