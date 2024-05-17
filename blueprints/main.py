import datetime

from flask import Blueprint, request, render_template
import Categories
from OpenTDB import OpenTDB
from app import token_required
from util.helper import get_user
from models import Round
from app import db

main = Blueprint('main', __name__)


@main.route("/trivia", methods=['GET'])
@token_required
def get_questions():
    category = Categories.GENERAL_KNOWLEDGE
    if "category" in request.args.keys():
        category = Categories.list[request.args['category'].upper()]

    total_questions = "10"
    if "total_questions" in request.args.keys():
        total_questions = request.args['total_questions']

    difficulty = "easy"
    if "difficulty" in request.args.keys():
        difficulty = request.args['difficulty']

    opentdb = OpenTDB()
    return opentdb.get(total_questions, category, difficulty)


@main.route("/submit", methods=['POST'])
@token_required
def submit_result():
    data = request.get_json()
    user = get_user()
    new_round = Round(
        user_id=user.id,
        points=data['points'],
        total_questions=data['total_questions'],
        correct_answers=data['correct_answers'],
        wrong_answers=data['wrong_answers'],
        difficulty=data['difficulty'],
        created_at=datetime.datetime.utcnow()
    )
    db.session.add(new_round)
    db.session.commit()
    return {'status': 0, 'message': 'round saved', "data": data}, 200


@main.route("/stats", methods=['GET'])
@token_required
def get_stats():
    user = get_user()
    rounds = Round.query.filter_by(user_id=user.id).all()
    stats = {
        'totals': {"points": 0, "questions": 0, "correct_answers": 0},
        'leaderboards': []
    }

    for round in rounds:
        stats['totals']['points'] += round.points
        stats['totals']['questions'] += round.total_questions
        stats['totals']['correct_answers'] += round.correct_answers

    return {'status': 0, 'data': stats}, 200

@main.route("/", methods=['GET'])
def index():
    return render_template('index.html',)
