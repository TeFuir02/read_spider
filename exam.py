from flask import Flask,render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy
from spider import Spider_Crawl
import config

spider = Spider_Crawl()
url = "http://www.xbiquge.la/"

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class Story(db.Model):
    __tablename__="story"
    id = db.Column(db.Integer,primary_key=True)
    url = db.Column(db.String(50))
    bookname = db.Column(db.String(30))

class Story_title(db.Model):
    __tablename__="story_title"
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    url = db.Column(db.String(50))
    content = db.Column(db.Text)
    s_id = db.Column(db.Integer,db.ForeignKey(Story.id))

@app.route("/")
def login():
    html = spider.get_url(url)
    detail_vote = spider.parse(html)

    for key in detail_vote.keys():
        # print(key)
        # print(detail_vote[key])
        s1 = Story(url = detail_vote[key],bookname=key)
        db.session.add(s1)
        db.session.commit()
    s = Story.query.all()
    return render_template("login.html",s=s)

@app.route("/content/<id>",methods=["GET","POST"])
def content(id):
    s = Story.query.filter(Story.id==id).first()
    html = spider.get_url(s.url)
    detail_d = spider.detail_parse(html)
    for j in detail_d.keys():
        detail_url = url + detail_d.get(j)
        # print("list",detail_url)
        content_text = spider.get_url(detail_url)
        # print("content_text",content_text)
        detail_text_content = spider.read_parse(content_text)
        # print("detail_text_content",detail_text_content)
        t = Story_title(title=j,url=detail_url,content=detail_text_content,s_id=s.id)
        db.session.add(t)
        db.session.commit()
    s_t = Story_title.query.filter(Story_title.s_id==id).all()
    return render_template("content.html",s_t =s_t)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(debug=True)