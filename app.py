import sqlite3 as sql

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        type = request.form.get("type")
        return redirect(f"/start-experiment/{first_name}/{type}")
    if request.method == "GET":
        return render_template('index.html')

@app.route('/start-experiment/<first_name>/<type>', methods=["GET"])
def startexperiment(first_name, type):
    if request.method == "GET":
        con = sql.connect("data.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM vacancies WHERE first_name==?;", (first_name,))

        vacancies = cur.fetchall()

        return render_template("start.html", jobseeker=vacancies, first_name=first_name, type=type)

@app.route('/volgende-ronde/ronde<round>/<jobseeker>/<group>', methods=["GET"])
def volgenderonde(round, jobseeker, group):
    if request.method == "GET":
        con = sql.connect("data.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("SELECT * FROM vacancies WHERE first_name==?;", (jobseeker,))

        vacancies = cur.fetchall()

        return render_template("newround.html", round=round, group=group, jobseeker=vacancies, first_name=jobseeker)

@app.route('/zoeken-mp/<first_name>', methods=["GET","POST"])
def advancedsearch(first_name):  # put application's code here
    if request.method == "POST":

        user_query = request.form.get("query")
        query = user_query.split()

        if len(query) == 1:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE first_name==? AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "ORDER BY matchingp DESC;",
                (first_name, "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[0] + "%"))

            results = cur.fetchall()

        if len(query) == 2:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE first_name==? AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "ORDER BY matchingp DESC;",
                (first_name, "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[0] + "%",
                 "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%",
                 "%" + query[1] + "%"))

            results = cur.fetchall()

        if len(query) == 3:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE first_name==? AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "ORDER BY matchingp DESC;",
                (first_name, "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[0] + "%",
                 "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%",
                 "%" + query[1] + "%",
                 "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%",
                 "%" + query[2] + "%"))

            results = cur.fetchall()

        if len(query) == 4:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE first_name==? AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "ORDER BY matchingp DESC;",
                (first_name, "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[0] + "%",
                 "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%",
                 "%" + query[1] + "%",
                 "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%",
                 "%" + query[2] + "%",
                 "%" + query[3] + "%", "%" + query[3] + "%", "%" + query[3] + "%", "%" + query[3] + "%",
                 "%" + query[3] + "%"
                 ))

            results = cur.fetchall()

        return render_template("search-advanced.html", results=results, query=query, first_name=first_name)

    if request.method == "GET":
        con = sql.connect("data.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute(
            "SELECT * FROM vacancies WHERE first_name==? AND (match==1)"
            "ORDER BY matchingp DESC;",
            (first_name,))

        perfect = cur.fetchall()

        cur.close()

        con = sql.connect("data.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute(
            "SELECT * FROM vacancies WHERE first_name==? AND match==0;",
            (first_name,))

        results = cur.fetchall()

        return render_template("search-advanced.html", perfect=perfect, results=results, first_name=first_name)

@app.route('/zoeken-zp', methods=["GET","POST"])
def manualsearch():  # put application's code here
    if request.method == "POST":
        user_query = request.form.get("query")
        query = user_query.split()

        if len(query) == 1:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?);",
                ("%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%","%" + query[0] + "%"))

            results = cur.fetchall()

        if len(query) == 2:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?);",
                ("%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%"))

            results = cur.fetchall()

        if len(query) == 3:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?);",
                ("%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%",
                 "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%"))

            results = cur.fetchall()

        if len(query) == 4:
            con = sql.connect("data.db")
            con.row_factory = sql.Row

            cur = con.cursor()
            cur.execute(
                "SELECT * FROM vacancies WHERE (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "AND (title LIKE ? OR company LIKE ? OR location LIKE ? OR text LIKE ? OR keywords LIKE ?)"
                "ORDER BY matchingp DESC;",
                ("%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%", "%" + query[0] + "%",
                 "%" + query[0] + "%",
                 "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%", "%" + query[1] + "%",
                 "%" + query[1] + "%",
                 "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%", "%" + query[2] + "%",
                 "%" + query[2] + "%",
                 "%" + query[3] + "%", "%" + query[3] + "%", "%" + query[3] + "%", "%" + query[3] + "%",
                 "%" + query[3] + "%"
                 ))

            results = cur.fetchall()

        return render_template("search-manual.html", results=results, query=user_query)

    if request.method == "GET":

        return render_template("search-manual.html")

if __name__ == '__main__':
    app.run()
