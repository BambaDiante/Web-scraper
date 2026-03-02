#ce code est le code source me permettant de configureer les routes de mon api
from flask import Flask, render_template,jsonify,request
import base
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("acceuil.html")

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