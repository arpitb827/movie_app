from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__,template_folder='../movie_app/templates')

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movie.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY']="hey1234"
db = SQLAlchemy(app)
class movie(db.Model):
     id = db.Column('movie_id', db.Integer, primary_key=True)
     name = db.Column(db.String(100))
     time = db.Column(db.String(50))
     location = db.Column(db.String(200))

     def __init__(self, name, time, location):
      	self.name = name
      	self.time = time
      	self.location = location

@app.route('/')
def movie_all():
   return render_template('index.html', movies=movie.query.all() )
    # return render_template('index.html', students=movie.query.all() )

@app.route('/delete_movie/<int:movie_id>')
def delete_movie(movie_id):
    id_to_delete = movie.query.filter_by(id=int(movie_id)).first()
    message = ""
    if id_to_delete:
      message+=str(id_to_delete.name)
      db.session.delete(id_to_delete)
      db.session.commit()
      flash(message+" "+"Deleted Sucessfully.")
    return render_template('index.html', movies=movie.query.all() )

@app.route('/edit_movie/<int:movie_id>',methods=['GET', 'POST'])
def edit_movie(movie_id,edit=False):
    search_result = movie.query.filter_by(id=int(movie_id)).first()
    exist_data = {}
    if search_result:
        exist_data.update({'name':search_result.name,'time':search_result.time,'location':search_result.location})
        #editing the movie details
        if request.method == 'POST':
          if not request.form['name'] or not request.form['time'] or not request.form['location']:
            flash('Please enter all the fields', 'error')
          else:
            Flag = False
            if request.form['name']!= search_result.name:
              search_result.name = request.form['name']
              db.session.add(search_result)
              db.session.commit()
              Flag=True
            elif request.form['time']!= search_result.time:
              search_result.time = request.form['time']
              db.session.add(search_result)
              db.session.commit()
              Flag=True
            elif request.form['location']!=search_result.location:
               search_result.location = request.form['location']
               db.session.add(search_result)
               db.session.commit()
               Flag=True
            else:
              Flag=False

            if Flag:
              flash('Movie is Edited Sucessfully!')
              return redirect(url_for('movie_all'))

    return render_template('edit_movie.html',data = [exist_data])


@app.route('/new', methods=['GET', 'POST'])
def add_movie():
   if request.method == 'POST':
     if not request.form['name'] or not request.form['time'] or not request.form['location']:
       flash('Please enter all the fields', 'error')
     else:
       movie_data = movie(request.form['name'],
       request.form['time'],
       request.form['location'],)
       db.session.add(movie_data)
       db.session.commit()
       flash('Movie is created Sucessfully!')
       return redirect(url_for('movie_all'))
   return render_template('add_movie.html')

if __name__ == '__main__':
  db.create_all()
  app.run(host='0.0.0.0',port=5001,debug=True)
