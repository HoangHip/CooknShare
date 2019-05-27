from flask import *
from foods_db import Users,Foods
from bson.objectid import ObjectId
app = Flask(__name__)

app.config['SECRET_KEY'] = '1$^f3DGDFEAK$#%@afkdfe'

@app.route('/home')
def home():
    return render_template('wellcome.html')
@app.route('/region')
def index():
    if 'logged' in session:
        if session['logged']:
            return render_template('home.html')
        else:
            return redirect('/login')
    else:
        return redirect('/login')            
@app.route('/asia/food')
def food():
    foods = Foods.find()
    return render_template('foods.html', foods = foods )

@app.route('/food/<id>')
def detail(id):
    food_detail = Foods.find_one({"_id": ObjectId(id)})
    return render_template('food_detail.html', food_detail = food_detail)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'logged' in session :
        if session['logged']:
            return redirect('/home')
        else:
            if request.method == 'GET':
                return render_template('login.html')
            elif request.method == 'POST':
                form = request.form
                login_username = form['login_username']
                login_password = form['login_password']
                user = Users.find_one({'username': login_username})
                if user is None:
                    session['logged'] = False
                    return redirect('/login')
                else:
                    if login_password == user['password']:
                        session['logged'] = True
                        session['name']= login_username
                        return redirect('/region')
                    else:
                        session['logged'] = False
                        return redirect('login')
    else:   
        session['logged'] = False
        return render_template('login.html')

@app.route('/logout')
def logout():
    if 'logged' in session:
        session['logged'] = False
    return redirect('/login')
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        form = request.form
        register_username = form['register_username']
        register_password = form['register_password']
        new_user = {
            'username' : register_username,
            'password' : register_password,
        }
        Users.insert_one(new_user)
        return redirect('/login')

@app.route('/search',methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    if request.method == 'POST':
        form = request.form
        search = form['search']
        foods = Foods.find()
        for food in foods:
            if search in food['Name']:
                foods = Foods.find({'Name':{'$regex' : search, "$options":'i'}})        
            elif search in food['Description']:
                foods = Foods.find({'Description':{'$regex' :  search, "$options":'i'}})
            # elif search in food['Type']:
                # foods = Foods.find({'Type':{'$regex' :  search}})
            elif search in food['Continent']:
                foods = Foods.find({'Continent':{'$regex' : search, "$options":'i'}})
            elif search in food['Ingredients']:
                foods = Foods.find({'Ingredients':{'$regex' : search, "$options":'i'}})
        #     # elif search in food['Steps']:
        #         # foods = Foods.find({'step':{'$regex' : search}})
            else :
                foods = None                        
        return render_template('search.html', foods= foods)

if __name__ == '__main__':
    app.run(debug=True)
 