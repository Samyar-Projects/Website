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


# ------- Libraries and utils -------
import datetime
from random import randint
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for, session
from flask_security import current_user
from modules.temp_data import QuizResultTemp, delete_quiz_res_temp, read_quiz_res_temp, write_quiz_res_temp
from utils.helpers import quiz_query_cond
from modules.database import QuizQuestions, db, QuizResults
from config import AppConfig
from init import cache, log
from flask_babel import gettext, get_locale


# ------- Blueprint init -------
quiz_pages = Blueprint("quiz_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Functions -------
def pop_sessions():
    session.pop("quiz.q_track")
    session.pop("quiz.q_left")
    session.pop("quiz.questions")
    session.pop("quiz.in_quiz")
    session.pop("quiz.quiz_id")


# ------- Page routes -------
@quiz_pages.route("/")
@cache.cached(timeout=AppConfig.RENDER_CACHE_TIMEOUT)
def index():
    """for i in range(0, 100):
        data = QuizQuestions("math", "en_US", 7, "normal", "This is placeholder question number " + str(i), "c", "Answer A", "Answer B", "Answer C", "Answer D", True)
        db.session.add(data)
        db.session.commit()"""

    return render_template("quiz_index.html")


@quiz_pages.route("/singleplayer", methods=["GET", "POST"])
def singleplayer():
    lang = str(get_locale())

    if not session.get("quiz.in_quiz"):
        if request.method == "POST":
            category = request.form.get("category-select")
            difficulty = request.form.get("difficulty-select")
            level = request.form.get("level-select")

            if not category or not difficulty or not level:
                log.debug(f"[{request.remote_addr}] Sent invalid quiz start request.")

                flash(gettext(u"Invalid input"), "danger")
                return redirect(url_for("quiz_pages.singleplayer"))

            questions = db.session.query(QuizQuestions.id).filter_by(lang=lang, category=category, difficulty=difficulty, level=int(level), status=True).all()

            if len(questions) < AppConfig.QUIZ_QUESTION_COUNT:
                log.debug(f"[{request.remote_addr}] Tried to start a quiz that does not exist.")

                flash(gettext(u"A quiz with these criteria does not exist."), "warning")
                return redirect(url_for("quiz_pages.singleplayer"))

            final_questions = []
            ids = []

            while len(final_questions) < AppConfig.QUIZ_QUESTION_COUNT:
                rand_id = randint(0, len(questions) - 1)
                question = questions[rand_id]

                if rand_id not in ids:
                    final_questions.append(question[0])
                    ids.append(rand_id)

            session["quiz.questions"] = final_questions
            session["quiz.q_track"] = 0
            session["quiz.q_left"] = AppConfig.QUIZ_QUESTION_COUNT - 1
            session["quiz.in_quiz"] = True

            q_id = randint(0, 999999999)

            while db.session.query(QuizResults).filter_by(quiz_id=q_id).first():
                q_id = randint(0, 999999999)

            session["quiz.quiz_id"] = q_id
            to_write = QuizResultTemp(0, 0, q_id)
            write_quiz_res_temp(to_write)

            log.debug(f"[{request.remote_addr}] Started a new quiz with Quiz ID: [{session.get('quiz.quiz_id')}]")

            return redirect(url_for("quiz_pages.singleplayer_quiz"))

        else:
            info = {"q_num": AppConfig.QUIZ_QUESTION_COUNT, "q_time": round(AppConfig.QUIZ_QUESTION_TIME / 60, 2)}
            return render_template("quiz/singleplayer.html", info=info)

    else:
        flash(gettext(u"You are already in a quiz. Please finish before starting a new one or click reset to reset it."), "danger")
        info = {"q_num": AppConfig.QUIZ_QUESTION_COUNT, "q_time": round(AppConfig.QUIZ_QUESTION_TIME / 60, 2), "reset_q": True}
        return render_template("quiz/singleplayer.html", info=info)


@quiz_pages.route("/multiplayer")
def multiplayer():
    return render_template("quiz/multiplayer.html")


@quiz_pages.route("/singleplayer-quiz", methods=["GET", "POST"])
def singleplayer_quiz():
    in_quiz = session.get("quiz.in_quiz")

    if in_quiz:
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

                    log.debug(f"[{request.remote_addr}] Sent answer [{answer}] for Quiz ID: [{session.get('quiz.quiz_id')}] with q_left [{q_left}] and q_track [{q_track}]")

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
                            data = read_quiz_res_temp(q_id)
                            data.set_right_answ(int(data.get_right_answ()) + 1)
                            write_quiz_res_temp(data)

                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer}

                            return render_template("quiz/singleplayer_quiz.html", question=send_question, info=info)

                        elif answ not in ["a", "b", "c", "d"]:
                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer}

                            return render_template("quiz/singleplayer_quiz.html", question=send_question, info=info)

                        else:
                            data = read_quiz_res_temp(q_id)
                            data.set_wrong_answ(int(data.get_wrong_answ()) + 1)
                            write_quiz_res_temp(data)

                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer, "answ": answ}

                            return render_template("quiz/singleplayer_quiz.html", question=send_question, info=info)

                    else:
                        pop_sessions()
                        delete_quiz_res_temp(q_id)

                        flash(gettext(u"Our anti-cheat systems have detected cheating! Please don't try to refresh or F12."), "danger")
                        return redirect(url_for("quiz_pages.singleplayer"))

                # Load next question:
                elif next and next.endswith(str(q_track)):
                    log.debug(f"[{request.remote_addr}] Requested next question for Quiz ID: [{session.get('quiz.quiz_id')}] with q_left [{q_left}] and q_track [{q_track}]")

                    question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id=get_q[q_left]).first())
                    answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id=get_q[q_left]).first())
                    answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id=get_q[q_left]).first())
                    answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id=get_q[q_left]).first())
                    answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id=get_q[q_left]).first())

                    session["quiz.q_track"] = q_track + 1
                    q_track = int(session.get("quiz.q_track"))

                    send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                    info = {"q_left": q_left + 1, "t_left": AppConfig.QUIZ_QUESTION_TIME, "q_track": q_track}

                    return render_template("quiz/singleplayer_quiz.html", question=send_question, info=info)

                else:
                    log.info(f"[{request.remote_addr}] Cheating detected for Quiz ID: [{session.get('quiz.quiz_id')}] at q_left [{q_left}] and q_track [{q_track}]")

                    pop_sessions()
                    delete_quiz_res_temp(q_id)

                    flash(gettext(u"Our anti-cheat systems have detected cheating! Please don't try to refresh or F12."), "danger")
                    return redirect(url_for("quiz_pages.singleplayer"))

            else:
                date_time = datetime.datetime.now()
                time = date_time.strftime("%H:%M")
                date = date_time.strftime("%d/%m/%Y")

                data = read_quiz_res_temp(q_id)

                if current_user.is_authenticated:
                    to_write = QuizResults(date, time, True, None, current_user.username, None, q_id, int(data.get_wrong_answ()), int(data.get_right_answ()), None, None)

                else:
                    to_write = QuizResults(date, time, False, None, "[AnonymousUser]", None, q_id, int(data.get_wrong_answ()), int(data.get_right_answ()), None, None)

                db.session.add(to_write)
                db.session.commit()

                log.debug(f"[{request.remote_addr}] Quiz completed with Quiz ID: [{session.get('quiz.quiz_id')}]")

                delete_quiz_res_temp(q_id)
                pop_sessions()

                return redirect(url_for("quiz_pages.show_results", q_id=q_id))

        # Load first question:
        else:
            if q_track == 0:
                log.debug(f"[{request.remote_addr}] Loaded first question with Quiz ID: [{session.get('quiz.quiz_id')}]")

                question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id=get_q[q_left]).first())
                answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id=get_q[q_left]).first())
                answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id=get_q[q_left]).first())
                answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id=get_q[q_left]).first())
                answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id=get_q[q_left]).first())

                send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                info = {"q_left": q_left + 1, "t_left": AppConfig.QUIZ_QUESTION_TIME, "q_track": q_track}

                session["quiz.q_track"] = q_track + 1
                q_track = int(session.get("quiz.q_track"))

                return render_template("quiz/singleplayer_quiz.html", question=send_question, info=info)

            else:
                return redirect(url_for("quiz_pages.singleplayer"))

    else:
        return redirect(url_for("quiz_pages.singleplayer"))


@quiz_pages.route("/singleplayer/reset-quiz")
def reset_quiz_singleplayer():
    log.debug(f"[{request.remote_addr}] Reset their singleplayer quiz. Quiz ID: [{session.get('quiz.quiz_id')}]")

    delete_quiz_res_temp(int(session.get("quiz.quiz_id")))
    pop_sessions()

    flash(gettext(u"Your quiz has been reset. You can now start a new quiz."), "success")
    return redirect(url_for("quiz_pages.singleplayer"))


@quiz_pages.route("/quiz-result/<q_id>")
def show_results(q_id):
    log.debug(f"[{request.remote_addr}] Requested quiz results for Quiz ID: [{q_id}]")

    try:
        p1_r_answ = quiz_query_cond(db.session.query(QuizResults.player_1_right).filter_by(quiz_id=q_id).first())
        p1_w_answ = quiz_query_cond(db.session.query(QuizResults.player_1_wrong).filter_by(quiz_id=q_id).first())
        p1_user = quiz_query_cond(db.session.query(QuizResults.player_1).filter_by(quiz_id=q_id).first())
        p1_w_acc = quiz_query_cond(db.session.query(QuizResults.player_1_with_account).filter_by(quiz_id=q_id).first())

        p2_r_answ = quiz_query_cond(db.session.query(QuizResults.player_2_right).filter_by(quiz_id=q_id).first())
        p2_w_answ = quiz_query_cond(db.session.query(QuizResults.player_2_wrong).filter_by(quiz_id=q_id).first())
        p2_user = quiz_query_cond(db.session.query(QuizResults.player_2).filter_by(quiz_id=q_id).first())
        p2_w_acc = quiz_query_cond(db.session.query(QuizResults.player_2_with_account).filter_by(quiz_id=q_id).first())

        is_multiplayer = quiz_query_cond(db.session.query(QuizResults.multiplayer).filter_by(quiz_id=q_id).first())
        date = quiz_query_cond(db.session.query(QuizResults.date).filter_by(quiz_id=q_id).first())
        time = quiz_query_cond(db.session.query(QuizResults.time).filter_by(quiz_id=q_id).first())

    except Exception:
        log.debug(f"[{request.remote_addr}] Requested quiz results for a quiz that does not exist.")
        abort(404)

    else:
        if is_multiplayer is not True:
            info = {"p1_r_answ": p1_r_answ, "p1_w_answ": p1_w_answ, "p1_user": p1_user, "p1_w_acc": p1_w_acc, "date": date, "time": time, "q_id": q_id, "q_num": AppConfig.QUIZ_QUESTION_COUNT, "show_modal": (str(get_locale()) == "tr_TR")}
            return render_template("quiz/result.html", info=info)

        else:
            info = {"p1_r_answ": p1_r_answ, "p1_w_answ": p1_w_answ, "p1_user": p1_user, "p1_w_acc": p1_w_acc, "p2_r_answ": p2_r_answ, "p2_w_answ": p2_w_answ, "p2_user": p2_user, "p2_w_acc": p2_w_acc, "date": date, "time": time, "q_id": q_id, "q_num": AppConfig.QUIZ_QUESTION_COUNT, "show_modal": False}
            return render_template("quiz/result.html", info=info)
