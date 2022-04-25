# Copyright 2022 Gigawhat Programming Team
# Quiz subdomain module.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#     
# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# ------- Libraries and utils -------
from random import randint
from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for, session
from init import cache
from utils.helpers import quiz_query_cond, translate
from modules.database import quiz_questions, db


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
q_num = 15    # Number of questions in a quiz
q_time = 60   # How many seconds to allow for one question


# ------- Page routes -------
@quiz_pages.route('/')
def index():
    return render_template(request.cookies.get("lang") + "/quiz_index.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

@quiz_pages.route('/singleplayer', methods = ["GET", "POST"])
def singleplayer():
    lang = request.cookies.get("lang")
    
    if request.method == "POST":
        category = request.form.get("category-select")
        difficulty = request.form.get("difficulty-select")
        level = request.form.get("level-select")
        
        if not category or not difficulty or not level:
            flash(translate("invalid_input", lang), "danger")
            return redirect(url_for("quiz_pages.singleplayer"))

        questions = db.session.query(quiz_questions.id).filter_by(lang = lang, category = category, difficulty = difficulty, level = int(level), status = True).all()
        
        if len(questions) < q_num :
            flash(translate("quiz_not_exist", lang), "warning")
            return redirect(url_for("quiz_pages.singleplayer"))
        
        final_questions = []
        ids = []
        
        while len(final_questions) < q_num:
            rand_id = randint(0, q_num - 1)
            question = questions[rand_id]
            
            if not rand_id in ids:
                final_questions.append(question[0])
                ids.append(rand_id)
        
        session["quiz.questions"] = final_questions
        session["quiz.current_q"] = 0
        session["quiz.q_left"] = 14
        session["quiz.in_quiz"] = True
        
        return redirect(url_for("quiz_pages.singleplayer_quiz"))
    
    else:
        info = {"q_num": q_num, "q_time": round(q_time / 60, 2)}
        return render_template(lang + "/quiz/singleplayer.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser", info = info)

@quiz_pages.route('/multiplayer')
def multiplayer():
    return render_template(request.cookies.get("lang") + "/quiz/multiplayer.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

@quiz_pages.route('/singleplayer-quiz', methods = ["GET", "POST"])
def singleplayer_quiz():
    in_quiz = session.get("quiz.in_quiz")
    
    if in_quiz:
        lang = request.cookies.get("lang")
        
        if request.method == "POST":
            next = request.form.get("next")
                
            current_q = int(session.get("quiz.current_q"))
            q_left = int(session.get("quiz.q_left"))
            get_q = session.get("quiz.questions")
                
            if not next:
                answer = request.form.get("answ")
                correct_answer = quiz_query_cond(db.session.query(quiz_questions.correct_answ).filter_by(id = get_q[q_left]).first())
                    
                if answer.endswith(str(current_q)):
                    question = quiz_query_cond(db.session.query(quiz_questions.question).filter_by(id = get_q[q_left]).first())
                    answ_a = quiz_query_cond(db.session.query(quiz_questions.answ_a).filter_by(id = get_q[q_left]).first())
                    answ_b = quiz_query_cond(db.session.query(quiz_questions.answ_b).filter_by(id = get_q[q_left]).first())
                    answ_c = quiz_query_cond(db.session.query(quiz_questions.answ_c).filter_by(id = get_q[q_left]).first())
                    answ_d = quiz_query_cond(db.session.query(quiz_questions.answ_d).filter_by(id = get_q[q_left]).first())
                        
                    answ = answer.split("answ_")
                    answ = answ[1]
                    answ = answ.split("_")
                    answ = answ[0]
                        
                    session["quiz.current_q"] = current_q + 1
                    current_q = int(session.get("quiz.current_q"))
                       
                    # Todo: Save number of right and wrong answers in temporary storage. 
                    if answ == correct_answer:
                        send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                        info = {"q_left": q_left + 1, "c_num": current_q, "correct_answ": correct_answer}
                    
                        return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)
                        
                    else:
                        send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                        info = {"q_left": q_left + 1, "c_num": current_q, "correct_answ": correct_answer, "answ": answ}
                    
                        return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)
        
                else:
                    session.pop("quiz.current_q")
                    session.pop("quiz.questions")
                    session.pop("quiz.in_quiz")
                        
                    flash(translate("anti_cheat_det", lang), "danger")
                    return redirect(url_for("quiz_pages.singleplayer"))
                
            elif next and next.endswith(str(current_q)):
                if not q_left < 0:
                    question = quiz_query_cond(db.session.query(quiz_questions.question).filter_by(id = get_q[q_left]).first())
                    answ_a = quiz_query_cond(db.session.query(quiz_questions.answ_a).filter_by(id = get_q[q_left]).first())
                    answ_b = quiz_query_cond(db.session.query(quiz_questions.answ_b).filter_by(id = get_q[q_left]).first())
                    answ_c = quiz_query_cond(db.session.query(quiz_questions.answ_c).filter_by(id = get_q[q_left]).first())
                    answ_d = quiz_query_cond(db.session.query(quiz_questions.answ_d).filter_by(id = get_q[q_left]).first())
        
                    session["quiz.current_q"] = current_q + 1
                    current_q = int(session.get("quiz.current_q"))
                        
                    session["quiz.q_left"] = q_left - 1
                    q_left = int(session.get("quiz.q_left"))
        
                    send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                    info = {"q_left": q_left + 1, "t_left": q_time, "c_num": current_q}

                    return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)
                    
                else:
                    # Todo: Move results from temporary storage to results database.
                    # Todo: Show quiz results.
                    return redirect(url_for("quiz_pages.singleplayer"))		
        
            else:
                session.pop("quiz.current_q")
                session.pop("quiz.questions")
                session.pop("quiz.in_quiz")
                    
                flash(translate("anti_cheat_det", lang), "danger")
                return redirect(url_for("quiz_pages.singleplayer"))
            
        else:
            current_q = int(session.get("quiz.current_q"))
            q_left = int(session.get("quiz.q_left"))
            get_q = session.get("quiz.questions")
            
            if current_q == 0:
                question = quiz_query_cond(db.session.query(quiz_questions.question).filter_by(id = get_q[0]).first())
                answ_a = quiz_query_cond(db.session.query(quiz_questions.answ_a).filter_by(id = get_q[0]).first())
                answ_b = quiz_query_cond(db.session.query(quiz_questions.answ_b).filter_by(id = get_q[0]).first())
                answ_c = quiz_query_cond(db.session.query(quiz_questions.answ_c).filter_by(id = get_q[0]).first())
                answ_d = quiz_query_cond(db.session.query(quiz_questions.answ_d).filter_by(id = get_q[0]).first())

                send_question = {"question": question, "answ_a": answ_a, "answ_b": answ_b, "answ_c": answ_c, "answ_d": answ_d}
                info = {"q_left": q_left + 1, "t_left": q_time, "c_num": "0"}

                return render_template(lang + "/quiz/singleplayer_quiz.html", question = send_question, info = info)

            else:
                return redirect(url_for("quiz_pages.singleplayer"))
                 
    else:
        return redirect(url_for("quiz_pages.singleplayer"))