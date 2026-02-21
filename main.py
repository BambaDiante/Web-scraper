from flask import Flask, render_template,jsonify
import base
app = Flask(__name__)
@app.route('/')
def index():
    return "Web scraper entre Jumia et Expat-Dakar"

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
    categories = base.get_category()
    produits=base.get_cat_from_source(source,category)
    return jsonify(produits)

@app.route("/compare/<nom_produit>")
def compare(nom_produit):
    resultats=base.compare(nom_produit)
    return jsonify({
        "query": nom_produit,
        "results": resultats
    })