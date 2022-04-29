#  Gigawhat Website quiz module.
#  Copyright 2022 Gigawhat Programming Team
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
from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for, session
from modules.temp_data import QuizResultTemp, delete_quiz_res_temp, read_quiz_res_temp, write_quiz_res_temp
from utils.helpers import quiz_query_cond, translate
from modules.database import QuizQuestions, db, QuizResults
from config import QUIZ_QUESTION_COUNT, QUIZ_QUESTION_TIME


# ------- Blueprint init -------
quiz_pages = Blueprint("quiz_pages", __name__, template_folder = "../templates", static_folder = "../static")


# ------- Cookie setters -------
@quiz_pages.route("/set_lang_en", methods = ["POST", "GET"])
def set_lang_en():
    if request.method == "POST":
        response = make_response(redirect(request.referrer))
        response.set_cookie("lang", "en_us")
        
        return response
    
    else:
        abort(404)
    
@quiz_pages.route("/set_lang_tr", methods = ["POST", "GET"])
def set_lang_tr():
    if request.method == "POST":
        response = make_response(redirect(request.referrer))
        response.set_cookie("lang", "tr_tr")
        
        return response
    
    else:
        abort(404)


# ------- Global variables -------
q_num = QUIZ_QUESTION_COUNT   # Number of questions in a quiz
q_time = QUIZ_QUESTION_TIME   # How many seconds to allow for one question


# ------- Functions -------
def pop_sessions():
    session.pop("quiz.q_track")
    session.pop("quiz.q_left")
    session.pop("quiz.questions")
    session.pop("quiz.in_quiz")
    session.pop("quiz.quiz_id")


# ------- Page routes -------
@quiz_pages.route('/')
def index():
    for i in range(0, 100):
        data = QuizQuestions("math", "en_us", 7, "normal", "This is placeholder question number " + str(i), "a", "Answer A", "Answer B", "Answer C", "Answer D", True)
        db.session.add(data)
        db.session.commit()
    
    return render_template(request.cookies.get("lang") + "/quiz_index.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

@quiz_pages.route('/singleplayer', methods = ["GET", "POST"])
def singleplayer():
    lang = request.cookies.get("lang")
    
    if not session.get("quiz.in_quiz"):
        if request.method == "POST":
            category = request.form.get("category-select")
            difficulty = request.form.get("difficulty-select")
            level = request.form.get("level-select")
            
            if not category or not difficulty or not level:
                flash(translate("invalid_input", lang), "danger")
                return redirect(url_for("quiz_pages.singleplayer"))

            questions = db.session.query(QuizQuestions.id).filter_by(lang = lang, category = category, difficulty = difficulty, level = int(level), status = True).all()
            
            if len(questions) < q_num :
                flash(translate("quiz_not_exist", lang), "warning")
                return redirect(url_for("quiz_pages.singleplayer"))
            
            final_questions = []
            ids = []
            
            while len(final_questions) < q_num:
                rand_id = randint(0, db.session.query(QuizQuestions).count() - 1)
                question = questions[rand_id]
                
                if not rand_id in ids:
                    final_questions.append(question[0])
                    ids.append(rand_id)
            
            session["quiz.questions"] = final_questions
            session["quiz.q_track"] = 0
            session["quiz.q_left"] = 14
            session["quiz.in_quiz"] = True
            
            q_id = randint(0, 999999999)
            
            while db.session.query(QuizResults).filter_by(quiz_id = q_id).first():
                q_id = randint(0, 999999999)
                
            session["quiz.quiz_id"] = q_id
            to_write = QuizResultTemp(0, 0, q_id)
            write_quiz_res_temp(to_write)
            
            return redirect(url_for("quiz_pages.singleplayer_quiz"))
        
        else:
            info = {"q_num": q_num, "q_time": round(q_time / 60, 2)}
            return render_template(lang + "/quiz/singleplayer.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser", info = info)

    else:
        flash(translate("already_in_quiz", lang), "danger")
        info = {"q_num": q_num, "q_time": round(q_time / 60, 2), "reset_q": True}
        return render_template(lang + "/quiz/singleplayer.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser", info = info)
 

@quiz_pages.route('/multiplayer')
def multiplayer():
    return render_template(request.cookies.get("lang") + "/quiz/multiplayer.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

@quiz_pages.route('/singleplayer-quiz', methods = ["GET", "POST"])
def singleplayer_quiz():
    in_quiz = session.get("quiz.in_quiz")
    
    if in_quiz:
        lang = request.cookies.get("lang")
        
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
                    correct_answer = quiz_query_cond(db.session.query(QuizQuestions.correct_answ).filter_by(id = get_q[q_left]).first())
                        
                    if answer.endswith(str(q_left + 1)):
                        question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id = get_q[q_left]).first())
                        answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id = get_q[q_left]).first())
                        answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id = get_q[q_left]).first())
                        answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id = get_q[q_left]).first())
                        answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id = get_q[q_left]).first())
                            
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
                        
                            return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)
                            
                        elif answ != "a" and answ != "b" and answ != "c" and answ != "d":
                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer}
                        
                            return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)
                        
                        else:
                            data = read_quiz_res_temp(q_id)
                            data.set_wrong_answ(int(data.get_wrong_answ()) + 1)
                            write_quiz_res_temp(data)
                            
                            send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                            info = {"q_left": q_left + 1, "q_track": q_track, "correct_answ": correct_answer, "answ": answ}
                        
                            return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)
            
                    else:
                        pop_sessions()
                        delete_quiz_res_temp(q_id)
                            
                        flash(translate("anti_cheat_det", lang), "danger")
                        return redirect(url_for("quiz_pages.singleplayer"))
                    
                # Load next question:
                elif next and next.endswith(str(q_track)):
                    question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id = get_q[q_left]).first())
                    answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id = get_q[q_left]).first())
                    answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id = get_q[q_left]).first())
                    answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id = get_q[q_left]).first())
                    answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id = get_q[q_left]).first())
            
                    session["quiz.q_track"] = q_track + 1
                    q_track = int(session.get("quiz.q_track"))
            
                    send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                    info = {"q_left": q_left + 1, "t_left": q_time, "q_track": q_track}

                    return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)		
            
                else:
                    pop_sessions()
                    delete_quiz_res_temp(q_id)
                        
                    flash(translate("anti_cheat_det", lang), "danger")
                    return redirect(url_for("quiz_pages.singleplayer"))

            else:
                # Todo: Show quiz results.
                date_time = datetime.datetime.now()
                time = date_time.strftime("%H:%M")
                date = date_time.strftime("%d/%m/%Y")
                
                data = read_quiz_res_temp(q_id)
                to_write = QuizResults(date, time, False, "NotLoggedIn", "", q_id, int(data.get_wrong_answ()), int(data.get_right_answ()), 0, 0)
                
                db.session.add(to_write)
                db.session.commit()
                
                delete_quiz_res_temp(q_id)
                pop_sessions()
                
                return redirect(url_for("quiz_pages.singleplayer"))
            
        # Load first question:
        else:       
            if q_track == 0:
                question = quiz_query_cond(db.session.query(QuizQuestions.question).filter_by(id = get_q[q_left]).first())
                answ_a = quiz_query_cond(db.session.query(QuizQuestions.answ_a).filter_by(id = get_q[q_left]).first())
                answ_b = quiz_query_cond(db.session.query(QuizQuestions.answ_b).filter_by(id = get_q[q_left]).first())
                answ_c = quiz_query_cond(db.session.query(QuizQuestions.answ_c).filter_by(id = get_q[q_left]).first())
                answ_d = quiz_query_cond(db.session.query(QuizQuestions.answ_d).filter_by(id = get_q[q_left]).first())

                send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                info = {"q_left": q_left + 1, "t_left": q_time, "q_track": q_track}

                return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)

            else:
                return redirect(url_for("quiz_pages.singleplayer"))
                 
    else:
        return redirect(url_for("quiz_pages.singleplayer"))
    
@quiz_pages.route('/reset-quiz')
def reset_quiz():
    delete_quiz_res_temp(int(session.get("quiz.quiz_id")))
    pop_sessions()
    
    flash(translate("quiz_reset_success", request.cookies.get("lang")), "success")
    return redirect(url_for("quiz_pages.singleplayer"))