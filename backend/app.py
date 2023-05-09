from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///vigie.db"

db.init_app(app)

ma = Marshmallow(app)

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'date')


article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, title, content):
        self.title = title
        self.content = content

# get all articles
@app.route('/get', methods = ['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

# access article by id
@app.route('/get/<id>/', methods = ['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

# add article to database
@app.route('/add', methods = ['POST'])
def add_article():
    title = request.json['title']
    content = request.json['content']

    articles = Articles(title, content)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)

# edit article data
@app.route(f'/update/<id>/', methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    content = request.json['content']

    article.title = title
    article.content = content
    
    db.session.commit()
    return article_schema.jsonify(article)


# delete article data
@app.route(f'/delete/<id>/', methods = ['DELETE'])
def delete_article(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)


if __name__ == "__main__":
    app.run(debug=True)
    

# create db tables
with app.app_context():
    db.create_all()