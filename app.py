from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.sogtrtv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

app.secret_key = "ABCED"

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/intro", methods=["POST"])
def intro_post():

    img_receive = request.form['img_give']
    name_receive = request.form['name_give']
    explanation_receive = request.form['explanation_give']
    mbti_receive = request.form['mbti_give']
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    doc = {
        'picture': img_receive,
        'name': name_receive,
        'intro': explanation_receive,
        'mbti': mbti_receive,
        'blog': url_receive,
        'good': comment_receive
    }

    db.introduce.insert_one(doc)
    
    return jsonify({'msg':'저장 완료!'})

@app.route("/intro", methods=["GET"])
def intro_get():

    all_members = list(db.introduce.find({},{'_id':False}))    

    return jsonify({'result': all_members})

@app.route('/intro/input')
def introInput():
    return render_template('popup.html')

@app.route('/introDelete', methods=["DELETE"])
def introDelete():

    name = request.form['name_give']

    db.introduce.delete_one({'name' : name})

    return jsonify({'msg':'삭제 완료!'})


@app.route('/introDetail/<name>', methods=['GET', 'POST'])
def introDetail(name):

    user = db.introduce.find_one({'name': name})

    return render_template('detail.html', temp=user)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)