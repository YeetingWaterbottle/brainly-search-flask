import urllib.parse
import bs4
from markupsafe import Markup
import requests
from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def query_results():
    target_url = "https://www.google.com/search?q="

    query_input = request.form["query_input"]
    query_site = request.form["query_site"]
    result_number = request.form["result_number"]

    if query_input != "":
        target_url += urllib.parse.quote_plus(query_input)

    if query_site != "":
        target_url += f"+site:{query_site}"

    if result_number != "":
        target_url += f"&num={result_number}"

    search_page = requests.get(target_url)

    soup = bs4.BeautifulSoup(search_page.text, "html.parser")

    links = soup.find_all("a")

    valid_links = []

    for link in links:
        if link['href'].startswith("/url?q=") and query_site in link['href']:
            valid_result = urllib.parse.unquote(
                link['href'].split("url?q=")[1].split("&sa=")[0])
            if valid_result not in valid_links:
                valid_links.append(valid_result)

    output = f"<strong>{target_url}</strong><br><br>"

    for link in valid_links[:-1]:
        output += f"<a target='_blank' rel='noopener noreferrer' href='{link}'>{link}</a><br><br>"

    output += f"<script>window.open('{valid_links[0]}', '_blank').focus()</script>"

    return render_template("index.html", result=Markup(output))


if __name__ == '__main__':
    app.run(debug=True)
