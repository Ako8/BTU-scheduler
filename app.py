from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import config

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

db = SQLAlchemy(app)


@app.route("/", methods=["GET", "POST"])
def home():
    print(config.api_key)
    htmls = []
    if request.method == "POST":
        html_txt = request.form.get("url")
        credit = request.form.get("credit")
        doc = BeautifulSoup(html_txt, "html.parser")
        rows = doc.find_all("tr")

        for row in rows:
            icon_ok_tag = row.find("i", class_="icon-ok")
            td_with_6_00 = row.find("td", string=f"{credit}.00")

            if icon_ok_tag and td_with_6_00:
                a_tags = row.find_all("a")
                for a_tag in a_tags:
                    href = a_tag.get("href")
                    text = a_tag.get_text(strip=True)

                    # Get the color from the Bootstrap class of  tag
                    tr_class = row.get("class", [])
                    color = tr_class[0] if tr_class else None

                    # Make a request to the href URL with the session

                    html = {"subject": text, "href": href, "color": color}
                    htmls.append(html)
        return render_template("home.html", htmls=htmls, credit=credit)

    return render_template("home.html", html=[])


if __name__ == "__main__":
    app.run(debug=True)
