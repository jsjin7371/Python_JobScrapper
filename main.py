from flask import Flask, redirect, render_template, request, send_file

from extractors.remoteok_scrap import extract_remoteok_jobs
from extractors.weworkremotely_scrap import extract_wwr_jobs
from file import save_to_file

app = Flask("JobScrapper")
db = {}


#home
@app.route("/")
def home():
  return render_template("home.html")


#search
@app.route("/search")
def search():
  keyword = request.args.get("keyword")

  if keyword is None:
    return redirect("/")

  if keyword in db:
    jobs = db[keyword]
  else:
    wwr = extract_wwr_jobs(keyword)
    remoteok = extract_remoteok_jobs(keyword)
    jobs = wwr + remoteok
    db[keyword] = jobs

  return render_template("search.html", keyword=keyword, jobs=jobs)


#export
@app.route("/export")
def export():
  keyword = request.args.get("keyword")
  if keyword is None:
    return redirect("/")

  if keyword not in db:
    return redirect(f"/search?keyword={keyword}")
  save_to_file(keyword, db[keyword])
  return send_file(f"{keyword}.csv", as_attachment=True)


app.run("0.0.0.0")
