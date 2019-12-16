from flaskblog.model import User,Post #since we are in a package now
from flask import render_template,url_for,flash,redirect,abort,request # therefore package name
from flaskblog.form import RegistrationForm,LoginForm, UpdateAccountForm, PostForm #should be use before the model name
from flaskblog import app,db,bcrypt
from flask_login import login_user,current_user,logout_user,login_required
import secrets
import os


@app.route("/")
@app.route("/home")
def home():
    posts=Post.query.all()   #getting all posts from db
    return render_template('home.html',posts=posts)

@app.route("/about")
def about():
    return render_template('about.html',title='about')


#for new users
@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:  #if a user is logedin then redirect to home
        return redirect(url_for('home'))

    form=RegistrationForm() #object of registerform

    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')  #convert our origional password
        #here new user is added to database
        user=User(username=form.username.data,email=form.email.data,password=hashed_password) #adding values to the class User and table user
        db.session.add(user)  #adding the data of class to db table
        db.session.commit()  #executing the changes in database
        flash('Your account has been created! You are now able to log in','success')
        return redirect(url_for('login'))
    #here the form object get its values
    return render_template('register.html',title='Register',form=form)  #here the data is entered to the RegistrationForm class


#for posts
@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:  #if a user is logedin then redirect to home
        return redirect(url_for('home'))

    form=LoginForm() # object of LoginForm class

    if form.validate_on_submit():
        #here 'user' is the object of the class User
        user=User.query.filter_by(email=form.email.data).first()  #search for the user
        if user and bcrypt.check_password_hash(user.password, form.password.data): #if user present and password match
            login_user(user,remember=form.remember.data)   #login user ,flask_login ,user is obj of current user
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful .Please check username and password','danger')
    #user enter their deaits and login
    return render_template('login.html',title='Login',form=form) #from object of LoginForm class


@app.route("/logout")
def logout():
    logout_user()  #from flask_login
    return redirect(url_for('home'))


#a fumction to save the picture to our folder and and rename it
def save_picture(form_picture):         #here the form_picture is the whole picture data 
    random_hex=secrets.token_hex(8)   #creating a random name for our pic
    _, f_ext=os.path.splitext(form_picture.filename)    #getting the extension of out picture , form_picture.filename gives the origional name of the pic
    picture_fn=random_hex + f_ext                       #joining the new name with the extension
    picture_path=os.path.join(app.root_path,'static/profile_pic',picture_fn)     #creating the path to where save the picture
    form_picture.save(picture_path)              #saving our form_picture to our picture_path        

    return picture_fn


@app.route("/account" , methods=['GET','POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)  #calling of function
            current_user.image_file=picture_file          #assigning the image to the db column
        current_user.username=form.username.data          #assign updated name to our db 
        current_user.email=form.email.data                #assign updated email to db
        db.session.commit()  #here saving the new updated data to db
        flash('your accousnt has been updated! ', 'success')
        return redirect(url_for('account'))
    #elif request.method == 'GET' :
    if current_user.is_authenticated:  #from flask login
        form.username.data = current_user.username   #from flask_login
        form.email.data = current_user.email
        image_file=url_for('static', filename = 'profile_pic/'+ current_user.image_file)
    return render_template('account.html',title='Account', image_file=image_file,form=form)


@app.route("/post/new", methods=['GET','POST'])
@login_required
def new_post():
    form=PostForm()
    if form.validate_on_submit():
        post=Post(title=form.title.data, content=form.content.data, author=current_user)   #data is fethed to Post class and db
        db.session.add(post)                                                                #author one is !! confusing
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html',title='New Post',form=form, legend='New Post')

@app.route("/post/<int:post_id>") #here we will recive postid in route
def post(post_id):
    post=Post.query.get_or_404(post_id) #specific single post , post_id  
    return render_template('post.html', title=post.title ,post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    return render_template('create_post.html', title="Update Post", form=form, legend='Update Post')    

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))