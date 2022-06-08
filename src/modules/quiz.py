#  Gigawhat Website quiz module.
#  Copyright 2022 Gigawhat Programming Team
#  Written by Samyar Sadat Akhavi, 2022.
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
Quiz module for the Gigawhat website.

The singleplayer and multiplayer quiz game system.

Notes
-----
The multiplayer system is not complete.
"""


# ------- Libraries and utils -------
import datetime
from random import randint
from typing import Union
from flask import Blueprint, Response, abort, flash, make_response, redirect, render_template, request, url_for, session
from flask_security import current_user
from utils.temp_data import SpQuizResultTemp, delete_sp_quiz_res_temp, read_sp_quiz_res_temp, write_sp_quiz_res_temp
from utils.helpers import quiz_query_cond
from modules.database import QuizQuestions, QuizResults
from config import AppConfig
from init import log, db, debug_log
from flask_babel import gettext, get_locale
from utils.models import QuizPlayerInfo, player_info_json


# ------- Blueprint init -------
quiz_pages = Blueprint("quiz_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Global variables -------
QUIZ_QUESTION_COUNT = AppConfig.QUIZ_QUESTION_COUNT
QUIZ_QUESTION_TIME = AppConfig.QUIZ_QUESTION_TIME


# -=-=-= Functions =-=-=-

# ---- Pop all session variables for singleplayer quiz ----
def pop_sessions_sp():
    session.pop("quiz.q_track")
    session.pop("quiz.q_left")
    session.pop("quiz.questions")
    session.pop("quiz.in_quiz")
    session.pop("quiz.quiz_id")
    

# ---- Cancel a quiz and flash a message (Called when cheating is detected) ----
def cheating_sp(quiz_id: Union[int, str]) -> Response:
    pop_sessions_sp()
    delete_sp_quiz_res_temp(quiz_id)

    flash(gettext(u"Our anti-cheat systems have detected cheating! Please don't try to refresh or F12."), "danger")
    return redirect(url_for("quiz_pages.singleplayer"))


# ---- Return a response with the "js_avail" cookie set to false. Only required for the quiz module ----
def response_js_false(resp: Response) -> Response:
    response = make_response(resp)
    response.set_cookie("js_avail", "False")
    return response


# ------- Page routes -------
@quiz_pages.route("/")
def index():
    """for i in range(0, 30):
       data = QuizQuestions("math", None, "en_US", 7, "normal", "This is placeholder question number " + str(i), "c", "Answer A", "Answer B", "Answer C", "Answer D", True)
       db.session.add(data)
       db.session.commit()"""

    return render_template("quiz_index.html")


@quiz_pages.route("/singleplayer", methods=["GET", "POST"])
def singleplayer():
    lang = str(get_locale())
    js_avail = request.cookies.get("js_avail")

    if not session.get("quiz.in_quiz"):
        if request.method == "POST" and js_avail == "True":
            category = request.form.get("category-select")
            subcategory = request.form.get("subcategory-select")
            difficulty = request.form.get("difficulty-select")
            level = request.form.get("level-select")
            
            cat_optgroup = category.split("-")
            category = cat_optgroup[1]
            cat_optgroup = cat_optgroup[0]

            if not category or not difficulty or not level or not subcategory:
                debug_log.debug(f"[{request.remote_addr}] Sent invalid quiz start request.")

                flash(gettext(u"Invalid input"), "danger")
                return response_js_false(redirect(url_for("quiz_pages.singleplayer")))

            if cat_optgroup == "gk":
                questions = db.session.query(QuizQuestions.id).filter_by(lang=lang, category=category, subcategory=subcategory, difficulty=difficulty, status=True).all()
                
            elif cat_optgroup == "ss":
                questions = db.session.query(QuizQuestions.id).filter_by(lang=lang, category=category, difficulty=difficulty, level=int(level), status=True).all()
                
            else:
                debug_log.debug(f"[{request.remote_addr}] Sent invalid quiz category optgroup")

                flash(gettext(u"Invalid input"), "danger")
                return response_js_false(redirect(url_for("quiz_pages.singleplayer")))

            if len(questions) < QUIZ_QUESTION_COUNT:
                debug_log.debug(f"[{request.remote_addr}] Tried to start a quiz that does not exist.")

                flash(gettext(u"A quiz with these criteria does not exist."), "warning")
                return response_js_false(redirect(url_for("quiz_pages.singleplayer")))

            final_questions = []
            ids = []

            while len(final_questions) < QUIZ_QUESTION_COUNT:
                rand_id = randint(0, len(questions) - 1)
                question = questions[rand_id]

                if rand_id not in ids:
                    final_questions.append(question[0])
                    ids.append(rand_id)

            session["quiz.questions"] = final_questions
            session["quiz.q_track"] = 0
            session["quiz.q_left"] = QUIZ_QUESTION_COUNT - 1
            session["quiz.in_quiz"] = True

            q_id = randint(0, 999999999)

            while db.session.query(QuizResults).filter_by(quiz_id=q_id).first():
                q_id = randint(0, 999999999)

            session["quiz.quiz_id"] = q_id
            to_write = SpQuizResultTemp(0, 0, q_id)
            write_sp_quiz_res_temp(to_write)

            debug_log.debug(f"[{request.remote_addr}] Started a new quiz with Quiz ID: [{q_id}]")

            return redirect(url_for("quiz_pages.singleplayer_quiz"))

        elif request.method == "POST" and js_avail == "False":
            debug_log.debug(f"[{request.remote_addr}] Tried to start a quiz without JavaScript")
            
            flash(gettext(u"The quiz system requires JavaScript to function correctly."), "warning")     
            return redirect(url_for("quiz_pages.singleplayer"))

        else:
            info = {"q_num": QUIZ_QUESTION_COUNT, "q_time": round(QUIZ_QUESTION_TIME / 60, 2)}
            return response_js_false(render_template("quiz/singleplayer.html", info=info))

    else:
        flash(gettext(u"You are already in a quiz. Please finish before starting a new one or click reset to reset it."), "danger")
        info = {"q_num": QUIZ_QUESTION_COUNT, "q_time": round(QUIZ_QUESTION_TIME / 60, 2), "reset_q": True}
        return response_js_false(render_template("quiz/singleplayer.html", info=info))


@quiz_pages.route("/multiplayer")
def multiplayer():
    return render_template("quiz/multiplayer.html")


@quiz_pages.route("/singleplayer-quiz", methods=["GET", "POST"])
def singleplayer_quiz():
    in_quiz = session.get("quiz.in_quiz")
    js_avail = request.cookies.get("js_avail")

    if in_quiz and js_avail == "True":
        q_track = int(session.get("quiz.q_track"))
        q_left = int(session.get("quiz.q_left"))
        get_q = session.get("quiz.questions")
        q_id = int(session.get("quiz.quiz_id"))

        if request.method == "POST":
            next = request.form.get("next")

            if not q_left < 0:
                # Check answer:
                if not next:
                    answer = request.form.get("answ")
                    correct_answer = quiz_query_cond(db.session.query(QuizQuestions.correct_answ).filter_by(id=get_q[q_left]).first())

                    debug_log.debug(f"[{request.remote_addr}] Sent answer [{answer}] for Quiz ID: [{q_id}] with q_left [{q_left}] and q_track [{q_track}]")

                    if answer.endswith(str(q_left + 1)):
                        question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id=get_q[q_left]).first())
                        answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id=get_q[q_left]).first())
                        answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id=get_q[q_left]).first())
                        answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id=get_q[q_left]).first())
                        answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id=get_q[q_left]).first())

                        answ = answer.split("answ_")
                        answ = answ[1]
                        answ = answ.split("_")
                        answ = answ[0]

                        session["quiz.q_track"] = q_track + 1
                        q_track = int(session.get("quiz.q_track"))

                        session["quiz.q_left"] = q_left - 1
                        q_left = int(session.get("quiz.q_left"))

                        if answ == correct_answer:
                            data = read_sp_quiz_res_temp(q_id)
                            data.right_answ = data.right_answ + 1
                            write_sp_quiz_res_temp(data)
                            
                            debug_log.debug(f"[{request.remote_addr}] Sent correct answer for Quiz ID: [{q_id}] with q_left [{q_left}] and q_track [{q_track}]")

                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer}

                            return response_js_false(render_template("quiz/singleplayer_quiz.html", question=send_question, info=info))

                        elif answ not in ["a", "b", "c", "d"]:
                            debug_log.debug(f"[{request.remote_addr}] Sent empty answer for Quiz ID: [{q_id}] with q_left [{q_left}] and q_track [{q_track}]")
                            
                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer}

                            return response_js_false(render_template("quiz/singleplayer_quiz.html", question=send_question, info=info))

                        else:
                            data = read_sp_quiz_res_temp(q_id)
                            data.wrong_answ = data.wrong_answ + 1
                            write_sp_quiz_res_temp(data)
                            
                            debug_log.debug(f"[{request.remote_addr}] Sent wrong answer for Quiz ID: [{q_id}] with q_left [{q_left}] and q_track [{q_track}]")

                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer, "answ": answ}

                            return response_js_false(render_template("quiz/singleplayer_quiz.html", question=send_question, info=info))

                    else:
                        debug_log.debug(f"[{request.remote_addr}] Cheating detected for Quiz ID: [{q_id}] at q_left [{q_left}] and q_track [{q_track}]")
                        return response_js_false(cheating_sp(q_id))

                # Load next question:
                elif next and next.endswith(str(q_track)):
                    debug_log.debug(f"[{request.remote_addr}] Requested next question for Quiz ID: [{q_id}] with q_left [{q_left}] and q_track [{q_track}]")

                    question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id=get_q[q_left]).first())
                    answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id=get_q[q_left]).first())
                    answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id=get_q[q_left]).first())
                    answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id=get_q[q_left]).first())
                    answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id=get_q[q_left]).first())

                    session["quiz.q_track"] = q_track + 1
                    q_track = int(session.get("quiz.q_track"))

                    send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                    info = {"q_left": q_left + 1, "t_left": QUIZ_QUESTION_TIME, "q_track": q_track}

                    return response_js_false(render_template("quiz/singleplayer_quiz.html", question=send_question, info=info))

                else:
                    debug_log.debug(f"[{request.remote_addr}] Cheating detected for Quiz ID: [{q_id}] at q_left [{q_left}] and q_track [{q_track}]")
                    return response_js_false(cheating_sp(q_id))

            else:
                pop_sessions_sp()
                
                date_time = datetime.datetime.now()
                time = date_time.strftime("%H:%M")
                date = date_time.strftime("%d/%m/%Y")

                data = read_sp_quiz_res_temp(q_id)
                list_data = []

                if current_user.is_authenticated:
                    list_data.append(player_info_json(QuizPlayerInfo(current_user.username, True, data.right_answ, data.wrong_answ)))
                    to_write = QuizResults(date, time, False, q_id, list_data)

                else:
                    list_data.append(player_info_json(QuizPlayerInfo("AnonymousUser", False, data.right_answ, data.wrong_answ)))
                    to_write = QuizResults(date, time, False, q_id, list_data)

                delete_sp_quiz_res_temp(q_id)

                db.session.add(to_write)
                db.session.commit()

                debug_log.debug(f"[{request.remote_addr}] Quiz completed with Quiz ID: [{q_id}]")

                return response_js_false(redirect(url_for("quiz_pages.show_results", q_id=q_id)))

        # Load first question:
        else:
            if q_track == 0:
                debug_log.debug(f"[{request.remote_addr}] Loaded first question with Quiz ID: [{q_id}]")

                question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id=get_q[q_left]).first())
                answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id=get_q[q_left]).first())
                answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id=get_q[q_left]).first())
                answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id=get_q[q_left]).first())
                answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id=get_q[q_left]).first())

                send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                info = {"q_left": q_left + 1, "t_left": QUIZ_QUESTION_TIME, "q_track": q_track}

                session["quiz.q_track"] = q_track + 1
                q_track = int(session.get("quiz.q_track"))

                return response_js_false(render_template("quiz/singleplayer_quiz.html", question=send_question, info=info))

            else:
                return response_js_false(redirect(url_for("quiz_pages.singleplayer")))

    elif js_avail == "False":        
        flash(gettext(u"The quiz system requires JavaScript to function correctly."), "warning")
        q_id = session.get("quiz.quiz_id")
        debug_log.debug(f"[{request.remote_addr}] JavaScript disabled mid-quiz with Quiz ID: [{q_id}]")
        pop_sessions_sp()
        
        if q_id:
            delete_sp_quiz_res_temp(q_id)
        
        return redirect(url_for("quiz_pages.singleplayer"))

    else:
        return response_js_false(redirect(url_for("quiz_pages.singleplayer")))


@quiz_pages.route("/singleplayer/reset-quiz", methods=["POST"])
def reset_quiz_singleplayer():
    q_id = session.get("quiz.quiz_id")
    debug_log.debug(f"[{request.remote_addr}] Reset their singleplayer quiz. Quiz ID: [{q_id}]")

    delete_sp_quiz_res_temp(q_id)
    pop_sessions_sp()

    flash(gettext(u"Your quiz has been reset. You can now start a new quiz."), "success")
    return redirect(url_for("quiz_pages.singleplayer"))


@quiz_pages.route("/quiz-result/<q_id>")
def show_results(q_id):
    debug_log.debug(f"[{request.remote_addr}] Requested quiz results for Quiz ID: [{q_id}]")

    try:
        p_info = db.session.query(QuizResults.player_info).filter_by(quiz_id=q_id).first()
        is_multiplayer = quiz_query_cond(db.session.query(QuizResults.multiplayer).filter_by(quiz_id=q_id).first())
        date = quiz_query_cond(db.session.query(QuizResults.date).filter_by(quiz_id=q_id).first())
        time = quiz_query_cond(db.session.query(QuizResults.time).filter_by(quiz_id=q_id).first())
        
        info = {"p_info": p_info[0], "date": date, "time": time, "q_id": q_id, "q_num": QUIZ_QUESTION_COUNT, "multiplayer": is_multiplayer, "show_modal": (str(get_locale()) == "tr_TR" and is_multiplayer is not True)}
        return render_template("quiz/result.html", info=info)

    except TypeError:
        debug_log.debug(f"[{request.remote_addr}] Attempted to get quiz results for a quiz that does not exist. Quiz ID: [{q_id}]")
        abort(404)

    except Exception:
        log.exception(f"[{request.remote_addr}] ShowQuizResultException, with input [{q_id}]")
        abort(500)