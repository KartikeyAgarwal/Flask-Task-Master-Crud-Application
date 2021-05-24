from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        content = db.Column(db.String, nullable=False)
        date_created = db.Column(db.DateTime, default= datetime.now())

        def __repr__(self):
            return '<Task %r>' %self.id


@app.route('/', methods=['POST','GET','PUT'])
def function():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:    
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your task"
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks=tasks)


@app.route('/delete/<int:id>', methods=['GET','DELETE'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        # del task_to_delete
        db.session.commit()
        return redirect('/')
    except:
        return "There was an error deleting that task"
        


@app.route('/update/<int:id>', methods=['PUT','GET','POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an error updating the task through POST method !"
    
    if request.method == 'GET':
        return render_template('/update.html', task = task)

    if request.method == 'PUT':
        task.content = request.json[str(id)]
        
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There is an error updating the task thorugh PUT method !"

    else:
        return "Method used not defined !"


if __name__ == "__main__":
    app.run(debug=True)
