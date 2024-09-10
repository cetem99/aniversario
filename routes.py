from flask import (render_template, request, Flask, Blueprint, url_for, redirect)
from DAO import *

routes = Blueprint("route", __name__, template_folder="FrontEnd/HTML")
app = Flask(__name__)

@routes.route("/get_dados")
def get():
    return render_template("Gerenciar.html")

@routes.route("/get_dados", methods=["POST"])
def post():
    nome = request.form.get("nome")
    create(nome)
    return redirect(url_for("route.data"))



'''@routes.route("/show_data/<nome>")
def data(nome):
    return render_template("Data.html", nome=nome)'''



