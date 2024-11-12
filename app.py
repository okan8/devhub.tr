from flask import Flask, render_template, request, jsonify,Response,make_response,redirect,url_for
import requests
import hashlib
import sqlite3
import os
import re
import random
import jwt
import datetime
from flask import Flask
from flask_mail import Mail, Message
import email_templates
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = '99cb8acd-e5da-42e6-8b88-4645fa91758c'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MEDIA_FOLDER'] = 'static/assets/media/'  # Folder to save uploaded files
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif',"mp4","mov"}
secret_key="99cb8acd-e5da-42e6-8b88-4645fa91758c"
DATABASE = 'users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'okannn123123@gmail.com'
app.config['MAIL_PASSWORD'] = 'mnyw qnhg hmpq xgnn'  # Use your generated app password here

mail = Mail(app)


def send_verification_email(email, template, tokenn=0):
    with app.app_context():
        msg = Message('DEVHUB.TR', sender="destek@devhub.tr", recipients=[email])
        msg.html = getattr(email_templates,template)(tokenn) 
        try:
            mail.send(msg)
            print("email gönderildi")
        except Exception as e:
            pass
def verify_captcha(token,secret):
    url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    payload = {
        'secret': secret,
        'response': token
    }
    response = requests.post(url, data=payload)
    result = response.json()
    return result.get("success", False)
def create_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # Enable row access by name
    return conn

def create_tables():
    with create_connection() as conn:
        cursor = conn.cursor()
        
        # Users table with social media columns
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    is_verified INTEGER DEFAULT 0,  -- 0 = Doğrulanmamış, 1 = Doğrulanmış
    bio TEXT,
    profile_picture TEXT DEFAULT 'default_profile_picture.png',
    youtube TEXT,
    linkedin TEXT,
    github TEXT,
    twitter TEXT,
    instagram TEXT,
    branch TEXT,
    last_2fa TEXT,
    fa INTEGER DEFAULT 0,  -- fa: 0 = Doğrulanmamış, 1 = Doğrulanmış
    code_2fa INTEGER
)''')


        
        cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT,
            description TEXT,
            media_path TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        # Visits table to track user visits
        cursor.execute('''CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            visit_time TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )''')
        
        # Comments table to store comments for projects
        cursor.execute('''CREATE TABLE IF NOT EXISTS project_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            project_id INTEGER,
            comment TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (project_id) REFERENCES projects(id)
        )''')
        
        conn.commit()




@app.route('/auth')
def index():
    return render_template('auth.html')
@app.route('/all_data', methods=['GET'])
def all_data():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        
        user_data = []
        for user in users:
            cursor.execute("SELECT * FROM projects WHERE user_id = ?", (user['id'],))
            projects = cursor.fetchall()
            user_data.append({
                'user_id': user['id'],
                'username': user['username'],
                'bio': user['bio'],
                'profile_picture': user['profile_picture'],
                'projects': [{'title': project['title'], 'description': project['description'], 'media_path': project['media_path']} for project in projects]
            })
    
    return jsonify(users=user_data)


    return jsonify(user_data)
@app.route('/update_branch', methods=['POST'])
def update_branch():
    userid=get_user_id(request.cookies["sec_token"])
    data = request.get_json()
    branch = data.get('branch')
    if not branch:
        return jsonify(message="Branch alanı boş olamaz!"), 400

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET branch = ? WHERE id = ?", (branch, userid))
        conn.commit()
    return jsonify(message="Branch başarıyla güncellendi!")
def statuss_get_2fa(userid):
    with create_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT fa FROM users WHERE id=?",(userid,))
        fa_status=cursor.fetchone()[0]
    return int(fa_status)
def generate_2FA_code():
    return random.randint(100000, 999999)
def get_2fa_number(userid):
    with create_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT code_2fa FROM users WHERE id=?",(userid,))
        fa_status=cursor.fetchone()[0]
    return int(fa_status)
def last_time(user_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT last_2FA FROM users WHERE id=?", ( user_id,))
        last_time=cursor.fetchone()[0]
    return last_time
def update_last_2fa(user_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET last_2FA=? WHERE id=?", (datetime.datetime.now(), user_id))
        conn.commit()
def update_2f(user_id, code):
    with create_connection() as conn:  # Automatically handles closing the connection
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET code_2fa=? WHERE id=?", (code, user_id))
        conn.commit()  # Commit changes to the database

@app.route("/verify_2FA_code")
def verify_2FA_code():
    userid=get_user_id(request.cookies["sec_token"])
    code=int(request.args.get("code").replace(" ",""))
    true_code=int(get_2fa_number(userid))
    if true_code==code:
        print("ewqeq")
        update_last_2fa(userid)
        print("dasdsa")
        return jsonify({"success":1})
    return jsonify({"success":0})
@app.route("/switch_2FA")
def switch_2FA():
    status=["kapatıldı","açıldı"]
    userid=get_user_id(request.cookies["sec_token"])
    status1=int(request.args.get("status"))
    if not(status1==0 or status1==1):
        return jsonify(message="geçersiz durum değeri")
    with create_connection() as conn:
        cursor=conn.cursor()
        cursor.execute("UPDATE users SET fa=? WHERE id=? ",(status1,userid))
    return jsonify(message=f"2FA {status[status1]}")
@app.route('/download_password/<path:password>', methods=['GET'])
def download_password(password):
    text_content = f"Your password: {password}\nPlease keep this safe; you won't be able to log in without it."
    response = Response(text_content)
    response.headers['Content-Disposition'] = 'attachment; filename=password.txt'
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response
@app.before_request
def before_requests():
    allowed_paths = {
        "direct": ["/", "/auth", "/login", "/register"],
        "starts": ["/@", "/static", "/download_password","/verify_mail_q/"]
    }
    try:
        if get_user_id(request.cookies.get("sec_token")) is not None and request.path in ["/auth", "/login", "/register","/verify_mail_q/"]:
            return redirect("/")
    except:
        pass
    if not (request.path in allowed_paths['direct'] or any(request.path.startswith(path) for path in allowed_paths["starts"])):
        try:
            if get_user_id(request.cookies.get("sec_token")) is None:
                error = {"name": "Erişim Engellendi", "desc": "Bu sayfaya girmek için giriş yapmanız veya kayıt olmanız gerekmektedir!"}
                return render_template("error.html", error=error), 401
        except:
            error = {"name": "Erişim Engellendi", "desc": "Bu sayfaya girmek için giriş yapmanız veya kayıt olmanız gerekmektedir!"}
            return render_template("error.html", error=error), 401
def jwt_token_gen(password):
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    expiration_time = current_utc_time + datetime.timedelta(hours=1)
    jwt_payload = {
        'pwd': password, 
        'exp': expiration_time 
    }
    token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')
    return token
def get_user_id(token):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        password = decoded["user_id"]
        return password
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None  
def get_mail(token):
    try:
        decoded = jwt.decode(token, secret_key, algorithms=["HS256"])
        password = decoded["email"]
        return password
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None  
valid_email_domains = [
    'gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'mail.com', 'protonmail.com'
]

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return False
    domain = email.split('@')[1]
    if domain not in valid_email_domains:
        return False
    return True

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify(message="E-posta ve şifre gereklidir!"), 400
    if not is_valid_email(email):
        return jsonify(message="Geçersiz e-posta sağlayıcı! Lütfen geçerli bir e-posta adresi kullanın."), 400
    if len(password) < 8:
        return jsonify(message="Şifre en az 8 karakter olmalıdır!"), 400
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (email, password, is_verified) VALUES (?, ?, ?)", 
                           (email, hashed_password, 0)) 
            conn.commit()
        token=generate_mail_token(email)
        send_verification_email(email,"verify_email",token)
        return jsonify(message="Kayıt başarılı!"), 200
    except sqlite3.IntegrityError:
        return jsonify(message="E-posta zaten mevcut!"), 400
def verify_password(stored_password, provided_password):
    if hashlib.sha256(provided_password.encode()).hexdigest()==stored_password:
        return True
    return False
def generate_mail_token(email):
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    expiration_time = current_utc_time + datetime.timedelta(minutes=15)  
    jwt_payload = {
        'email': email,
        'exp': expiration_time 
    }
    token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')
    return token
def generate_jwt_token(user_id):
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    expiration_time = current_utc_time + datetime.timedelta(hours=1)  
    jwt_payload = {
        'user_id': user_id,
        'exp': expiration_time 
    }
    token = jwt.encode(jwt_payload, secret_key, algorithm='HS256')
    return token
@app.route("/verify_mail_q/<path:token>")
def verify_mail(token):
    mail = get_mail(token)
    if not mail:
        return "Invalid or expired token", 400
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET is_verified = ? WHERE email = ?", (1, mail))
            conn.commit() 
            if cursor.rowcount == 0:
                return "User not found or already verified", 404 
            return render_template("verified.html"), 200 
    except Exception as e:
        return f"An error occurred: {e}", 500
def get_mail_status(userid):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_verified FROM users WHERE id=?", (userid,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify(message="E-posta ve şifre gereklidir!"), 400
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email=?", (email,))
        user = cursor.fetchone()
    if user is None:
        return jsonify(message="Kullanıcı bulunamadı!"), 400
    stored_password = user[2]
    if not verify_password(stored_password, password):
        return jsonify(message="Geçersiz şifre!"), 400
    user_id = user[0] 
    token = generate_jwt_token(user_id)
    response = make_response({"message": "Giriş başarılı!", "token": token})
    response.set_cookie("sec_token", token, max_age=60*60)  # Tokeni cookie olarak sakla
    return response
URL_PATTERNS = {
    'youtube': r'https?://(www\.)?youtube\.com/@[\w-]+',  # YouTube kanal linki
    'linkedin': r'https?://(www\.)?linkedin\.com/in/[\w-]+',
    'github': r'https?://(www\.)?github\.com/[\w-]+',
    'twitter': r'https?://(www\.)?x\.com/[\w-]+',
    'instagram': r'https?://(www\.)?instagram\.com/[\w-]+'
}
@app.route('/update_social_media', methods=['POST'])
def update_social_media():
    userid=get_user_id(request.cookies["sec_token"])
    # Get the data from the request
    data = request.get_json()
    youtube = data.get('youtube')
    linkedin = data.get('linkedin')
    github = data.get('github')
    twitter = data.get('twitter')
    instagram = data.get('instagram')
    for platform, url in [('youtube', youtube), ('linkedin', linkedin), ('github', github), 
                           ('twitter', twitter), ('instagram', instagram)]:
        if url and not re.match(URL_PATTERNS.get(platform), url):
            return jsonify(message=f"Geçersiz {platform.capitalize()} linki!"), 400
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE users SET youtube = ?, linkedin = ?, github = ?, twitter = ?, instagram = ?
                          WHERE id = ?''',
                       (youtube, linkedin, github, twitter, instagram, userid))
        conn.commit()
    return jsonify(message="Sosyal medya bilgileri güncellendi!")

def check_2fa_expiry(last_2fa):
    if last_2fa is None:
        return False
    last_time = datetime.datetime.strptime(last_2fa, "%Y-%m-%d %H:%M:%S.%f")
    current_time = datetime.datetime.now()
    time_diff = current_time - last_time
    if time_diff <= datetime.timedelta(hours=1):
        return True
    else:
        return False
@app.route('/dashboard', methods=['GET'])
def dashboard():
    userid=get_user_id(request.cookies["sec_token"])
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT username,branch,bio, profile_picture, youtube, linkedin, github, twitter, instagram,email
                          FROM users WHERE id = ?''', (userid,))
        user_data = cursor.fetchone()

    if user_data is None:
        return jsonify(message="Kullanıcı bulunamadı!"), 404

    bio = user_data['bio'] if user_data['bio'] else "Henüz bir bio açıklaması yok."
    social_media = {
        'youtube': user_data['youtube'],
        'linkedin': user_data['linkedin'],
        'github': user_data['github'],
        'twitter': user_data['twitter'],
        'instagram': user_data['instagram']
    }
    status=get_mail_status(userid)
    if status==None or status==0:
        return render_template('verify.html')
    if user_data["username"] is None:
        return render_template('set_username.html')
    status_2fa=statuss_get_2fa(userid)
    fa_is_secure=int(check_2fa_expiry(last_time(userid)))
    if not fa_is_secure and status_2fa:
        scode=generate_2FA_code()
        update_2f(userid,scode)
        send_verification_email(user_data['email'],"code_2fa",scode)
        
    return render_template('dashboard.html', 
                           username=user_data['username'], 
                           bio=bio, 
                           user_profile_picture_url=user_data['profile_picture'],
                           social_media=social_media,branch=user_data["branch"],status_2fa=int(status_2fa),fa_is_secure=fa_is_secure)
@app.route('/set_username', methods=['POST'])
def set_username():
    data = request.get_json()
    username = data.get('username')
    userid=get_user_id(request.cookies["sec_token"])
    if not username:
        return jsonify(message="Kullanıcı adı boş olamaz!"), 400
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        return jsonify(message="Kullanıcı adı sadece harf ve rakamlardan oluşabilir, boşluk veya özel karakter içeremez!"), 400

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            return jsonify(message="Kullanıcı adı zaten alınmış!"), 400

        cursor.execute("UPDATE users SET username = ? WHERE id = ?", (username,userid ))
        conn.commit()

    return jsonify(message="Kullanıcı adı başarıyla ayarlandı!")

@app.route('/upload_project', methods=['POST'])
def upload_project():
    userid=get_user_id(request.cookies["sec_token"])


    # Get form data and file from request
    title = request.form.get('title')
    description = request.form.get('description')
    media_file = request.files.get('media')

    # Validate input fields
    if not title:
        return jsonify(message="Başlık boş olamaz!"), 400
    if not description:
        return jsonify(message="Açıklama boş olamaz!"), 400
    if not media_file:
        return jsonify(message="Medya dosyası boş olamaz!"), 400

    # Validate length of text fields
    if len(title) > 50:
        return jsonify(message="Başlık 50 karakterden uzun olamaz!"), 400
    if len(description) > 250:
        return jsonify(message="Açıklama 250 karakterden uzun olamaz!"), 400

    # Check if file type is allowed
    if not allowed_file(media_file.filename):
        return jsonify(message="Dosya türüne izin verilmiyor!"), 400

    # Secure the filename and save the file
    filename = secure_filename(media_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    media_file.save(file_path)

    # Insert project data into the database
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO projects (user_id, title, description, media_path) VALUES (?, ?, ?, ?)",
            (userid, title, description, file_path)
        )
        conn.commit()

    return jsonify(message="Proje yüklendi!")

@app.route('/api/view_my_bio', methods=['GET'])
def view_my_bio():
    userid=get_user_id(request.cookies["sec_token"])
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT bio FROM users WHERE id = ?", (userid,))
        user = cursor.fetchone()

    if user:
        return jsonify(bio=user['bio'])
    return jsonify(bio=None)

# Get projects
@app.route('/get_projects', methods=['GET'])
def get_projects(userid1=None):
    if userid1 is not None:
        userid = userid1
    else:
        userid = userid=get_user_id(request.cookies["sec_token"])


    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE user_id = ?", (userid,))
        projects = cursor.fetchall()

    return jsonify(projects=[{
        'title': project['title'],
        'description': project['description'],
        'media_path': project['media_path']
    } for project in projects])


# Logout
@app.route('/logout', methods=['POST'])
def logout():
    response = make_response(redirect('/'))
    response.set_cookie('sec_token', '', max_age=0)
    return response
@app.route('/update_bio', methods=['POST'])
def update_bio():
    userid=get_user_id(request.cookies["sec_token"])


    data = request.get_json()
    bio = data.get('bio')

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET bio = ? WHERE id = ?", (bio,userid))
        conn.commit()

    return jsonify(message="Bio güncellendi!")

@app.route('/upload_profile_picture', methods=['POST'])
def upload_profile_picture():
    userid=get_user_id(request.cookies["sec_token"])


    if 'file' not in request.files:
        return jsonify(message="Dosya yok!"), 400

    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify(message="Geçersiz dosya!"), 400

    filename = f"{userid}_{file.filename}"
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET profile_picture = ? WHERE id = ?", (filename,userid))
        conn.commit()

    return jsonify(message="Profil fotoğrafı yüklendi!", filename=filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_user_profile_picture():
    userid=get_user_id(request.cookies["sec_token"])
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT profile_picture FROM users WHERE id = ?", (userid,))
        result = cursor.fetchone()
    return result['profile_picture'] if result else None
@app.route("/")
def xcv():
    pageData = []
    try:
        user_id = get_user_id(request.cookies.get("sec_token"))
        if user_id:
            pageData = ["Dashboard", "/dashboard"]
        else:
            pageData = ["Bio oluştur", "/auth"]
    except Exception as e:
        app.logger.error(f"Error fetching user ID: {e}")
        pageData = ["Bio oluştur", "/auth"]
    
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
    
    return render_template("index.html", userCount=user_count, pageData=pageData)

@app.errorhandler(404)
def page_not_found(e):
    error={"name":"Sayfa bulunamadı.","desc":"Üzgünüz aradığınız sayfa sitemizde mevcut değil. :(("}
    return render_template('error.html',error=error), 404
@app.route("/@<path:username>")
def user_bio(username):
    user_data = {}
    theme=request.args.get("image")
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()

    if user is None:
        error = {"name": "Kullanıcı Bulunamadı.", "desc": "Üzgünüz, aradığınız kullanıcı mevcut değil!"}
        return render_template("error.html", error=error), 404

    cursor.execute("SELECT * FROM projects WHERE user_id = ?", (user["id"],))
    projects = cursor.fetchall()

    social_links = []
    if user['youtube']:
        social_links.append({'name': 'youtube', 'url': user['youtube'], 'icon': 'fab fa-youtube', 'color': 'text-red-600', 'hover_color': 'hover:text-red-600'})
    if user['linkedin']:
        social_links.append({'name': 'linkedin', 'url': user['linkedin'], 'icon': 'fab fa-linkedin', 'color': 'text-blue-700', 'hover_color': 'hover:text-blue-500'})
    if user['github']:
        social_links.append({'name': 'github', 'url': user['github'], 'icon': 'fab fa-github', 'color': 'text-gray-800', 'hover_color': 'hover:text-gray-600'})
    if user['twitter']:
        social_links.append({'name': 'twitter', 'url': user['twitter'], 'icon': 'fab fa-twitter', 'color': 'text-blue-400', 'hover_color': 'hover:text-blue-600'})
    if user['instagram']:
        social_links.append({'name': 'instagram', 'url': user['instagram'], 'icon': 'fab fa-instagram', 'color': 'text-pink-500', 'hover_color': 'hover:text-pink-400'})
    visit_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    cursor.execute('''INSERT INTO visits (user_id, visit_time) 
                      VALUES (?, ?)''', 
                   (user["id"], visit_time,))
    conn.commit()
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
        cursor.execute('''SELECT COUNT(*) FROM visits WHERE user_id = ? AND strftime('%Y-%m-%d', visit_time) = strftime('%Y-%m-%d', 'now')''', (user["id"],))
        visit_count = cursor.fetchone()[0]
    user_data = {
        'visitCount':visit_count,
        'branch': user["branch"],
        'user_id': user["id"],
        'username': user['username'],
        'bio': user["bio"],
        'profile_picture': user['profile_picture'],
        'social_links': social_links,
        'projects': [{'title': project['title'], 'description': project['description'], 'media_path': project['media_path']} for project in projects]
    }
    return render_template("bio_view.html", user=user_data,theme=theme)
@app.route('/get-visit-data', methods=['GET'])
def get_visit_data():
    username = request.args.get('username')
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user is None:
            return jsonify({'error': 'Kullanıcı bulunamadı'}), 404
        cursor.execute('''SELECT COUNT(*) FROM visits WHERE user_id = ? AND strftime('%Y-%m-%d', visit_time) = strftime('%Y-%m-%d', 'now')''', (user["id"],))
        visit_count = cursor.fetchone()[0]
        cursor.execute('''SELECT strftime('%H', visit_time) AS hour, COUNT(*) AS visit_count
                          FROM visits
                          WHERE user_id = ?
                          GROUP BY hour
                          ORDER BY hour''', (user["id"],))
        hourly_data = cursor.fetchall()
        hourly_visits = {
            'labels': [str(i).zfill(2) for i in range(24)], 
            'data': [0] * 24
        }
        for hour, count in hourly_data:
            index = int(hour)
            hourly_visits['data'][index] = count
    return jsonify({
        'visitCount': visit_count,
        'hourlyVisits': hourly_visits

    })

if __name__ == '__main__':
    create_tables()
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 
    app.run(port=3131
    ,debug=True)
    
#bitti :)