# backend/routes/technician.py
from flask import Blueprint, request, jsonify
from db_connection import get_connection
from models.technician import Technician

technician_bp = Blueprint("technician_bp", __name__)

@technician_bp.route('/technicians', methods=['GET'])
def get_technicians():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM technicians")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    technicians = [Technician(row).to_dict() for row in rows]
    return jsonify({"technicians": technicians})

@technician_bp.route('/technicians/recommend', methods=['GET'])
def recommend_technicians():
    skill_query = request.args.get('skill', '').strip().lower()
    max_price = float(request.args.get('max_price', 1000))
    location_query = request.args.get('location', '').strip().lower()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM technicians")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    results = []
    for row in rows:
        tech = Technician(row).to_dict()
        skills = [s.strip().lower() for s in tech['skills'].split(',')]

        if skill_query and not any(skill_query in s for s in skills):
            continue
        if tech['price_rate'] > max_price:
            continue
        if location_query and location_query not in tech['location'].lower():
            continue

        # Scoring
        rating_score = tech['avg_rating'] / 5
        exp_score = min(tech['experience_years'] / 20, 1)
        price_score = max(0, 1 - (tech['price_rate'] / 50))
        tech['score'] = round(0.4 + rating_score * 0.3 + exp_score * 0.2 + price_score * 0.1, 2)

        results.append(tech)

    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({"recommendations": results[:10]})
