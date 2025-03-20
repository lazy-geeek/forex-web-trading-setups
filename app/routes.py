from flask import Blueprint, render_template, request
from .scraping.extractor import run_scraping
from .ai.gemini_processor import process_setups

main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def dashboard():
    setups = []
    if request.method == "POST":
        raw_data = run_scraping()
        print("Debug: raw_data:", raw_data)
        setups = process_setups(raw_data)
    return render_template("dashboard.html", setups=setups)
