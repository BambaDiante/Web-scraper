#ce code est le code source me permettant de configureer les routes de mon api
from flask import Flask, render_template,jsonify,request,redirect,flash,url_for,session
import base
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_dance.contrib.google import make_google_blueprint, google
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = Flask(__name__)
app.secret_key='%##!t09144KVcn021@%d@nXt8&4%wP'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///utilisateurs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # On retire unique=True ici pour accepter les doublons de noms
    username = db.Column(db.String(20), nullable=False)
    # On garde unique=True ici car l'email doit rester unique
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
#plan de google
google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_url="http://127.0.0.1:5000/home",
    scope=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid"
    ]
)
app.register_blueprint(google_bp, url_prefix="/login")

@app.route('/')
def index():
    return render_template("loginpage.html")

@app.route('/search/<nom_produit>')
def search(nom_produit):
    categories = base.get_category()
    produits=base.get_product(nom_produit,categories)
    if produits:
        return jsonify({
            "query": nom_produit,
            "results": produits
        })
    else:
        return "Aucun produit trouve"

@app.route("/<source>/<category>")
def select(source,category):
    produits=base.get_cat_from_source(source,category)
    return jsonify(produits)

@app.route("/compare/<nom_produit>")
def compare(nom_produit):

    categories = base.get_category()
    produits=base.get_product(nom_produit,categories)
    
    return jsonify({
        "query": nom_produit,
        "results": produits
    })

@app.route("/rechercher",methods =['GET','POST'])
def rechercher():
    if request.method=="POST":
        #si le formulaire a ete envoyee
        donnees = request.form
        produit=donnees.get("produit recherche")       
        categories = base.get_category()
        produits=base.get_product(produit,categories)
        # print(produits)
    else:
        #si on est a la methode get 
        produits=None
    return render_template("recherche.html", resultats=produits)


@app.route("/home")
def home():
    # 1. On vérifie si l'authentification Google est active
    if not google.authorized:
        return redirect(url_for("google.login"))

    # 2. On récupère les infos du profil Google
    resp = google.get("/oauth2/v2/userinfo")
    if resp.ok:
        google_info = resp.json()
        email = google_info["email"]
        name = google_info.get("name", email)  # Récupère le nom, sinon utilise l'email

        #On cherche si l'utilisateur existe déjà dans ta base SQLAlchemy
        user = User.query.filter_by(email=email).first()

        # SI L'UTILISATEUR N'EXISTE PAS -> CRÉATION AUTOMATIQUE (Inscription)
        if not user:
            # Création dans utilisateurs.db (SQLAlchemy)
            # On met un mot de passe fictif car l'authentification se fait via Google
            user = User(username=name, email=email, password="GOOGLE_USER_NO_PASSWORD")
            db.session.add(user)
            db.session.commit()

            # synchronisation avec la bas secondaire
            base.enregister(name, email, "Inscrit via Google", "2000-01-01", "00000000", "GOOGLE_AUTH")

            flash("Bienvenue ! Votre compte a été créé automatiquement avec Google.", "success")

        # 5. CONNEXION OFFICIELLE
        login_user(user)
        session['username'] = user.username

        # 6. ENVOI VERS LA PAGE D'ACCUEIL
        return redirect(url_for('homepage'))

    # Si la réponse Google n'est pas OK
    flash("Échec de la connexion avec Google. Veuillez réessayer.", "danger")
    return redirect(url_for('login'))

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    if request.method == "POST":
        formulaire = request.form
        name = formulaire.get("name")
        email = formulaire.get("mail")
        password = formulaire.get("password")

        # Champs spécifiques pour la base secondaire (base.py)
        adresse = formulaire.get("adresse")
        date_n = formulaire.get("date")
        phone = formulaire.get("telephone")

        # 1. Vérification d'unicité de l'email dans SQLAlchemy
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash("Cet email est déjà utilisé. Connectez-vous ou utilisez un autre mail.", "danger")
            return redirect(url_for('login'))

        #inscription dans ma base secondaire
        base.enregister(name, email, adresse, date_n, phone, password)

        #inscription dans ma base principale
        new_user = User(username=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        # 4. CONNEXION AUTOMATIQUE
        login_user(new_user)
        session['username'] = name

        flash("Compte créé avec succès !", "success")
        return redirect(url_for('homepage'))

    # Si on arrive en GET (en tapant l'URL), on affiche le formulaire
    return render_template("loginpage.html")
@app.route("/homepage")
@login_required
def homepage():
    return render_template("homepage.html", name=current_user.username)
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get("mail")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            login_user(user)
            session['username'] = user.username
            return redirect(url_for('homepage'))
        else:
            flash('Email ou mot de passe incorrect.', 'danger')
            return redirect(url_for('login'))  # On reste sur le login !
    return render_template("loginpage.html")

@app.route("/logout")
def logout():
    logout_user()
    flash('Vous avez ete deconnecte.', 'info')
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("mail")
        password = request.form.get("password")
        # Vérifier si l'utilisateur existe déjà
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            flash('Cet email est déjà utilisé.', 'danger')
            return redirect(url_for('register'))

        # Création du nouvel utilisateur
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Compte créé avec succès ! Vous pouvez vous connecter.', 'success')
        return redirect(url_for('login'))

    return render_template("loginpage.html")
