import re

from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError


pages_bp = Blueprint("pages", __name__)
api_bp = Blueprint("api", __name__)


@pages_bp.route("/")
def ana_sayfa():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json(silent=True) or {}
    mesaj = data.get("mesaj", "").strip()
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alani zorunludur."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    except AIServiceError:
        return jsonify({
            "basari": False,
            "hata": "Yapay zeka servisine su anda ulasilamiyor."
        }), 503


@api_bp.route("/leads", methods=["POST"])
def lead_olustur():
    data = request.get_json(silent=True) or {}

    if not isinstance(data, dict) or any(
        not isinstance(data.get(alan, ""), str)
        for alan in ("isim", "telefon", "eposta", "mesaj")
    ):
        return jsonify({"basari": False, "hata": "Form alanlari metin olmalidir."}), 400

    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    eposta = data.get("eposta", "").strip()
    mesaj = data.get("mesaj", "").strip()

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "Isim ve telefon zorunludur."
        }), 400

    if eposta and not re.fullmatch(r"[^\s@]+@[^\s@]+\.[^\s@]+", eposta):
        return jsonify({"basari": False, "hata": "Gecerli bir e-posta adresi girin."}), 400

    if len(isim) > 150 or len(telefon) > 40 or len(eposta) > 254 or len(mesaj) > 5000:
        return jsonify({"basari": False, "hata": "Form alanlari cok uzun."}), 400

    lead_ekle(isim, telefon, mesaj, eposta)

    return jsonify({
        "basari": True,
        "mesaj": "Kaydiniz basariyla alindi."
    }), 201


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    return jsonify({
        "basari": True,
        "leads": tum_leadler()
    })