from flask import Flask, render_template, request, jsonify, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.sogtrtv.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import base64
import gridfs
fs = gridfs.GridFS(db)

@app.route('/')
def home():
    return render_template('index.html')

# 클라이언트가 서버에 이미지 정보 업로드
@app.route('/intro', methods=['POST'])
def intro_post():
    img_receive = request.files["img_give"]
    name_receive = request.form["name_give"]
    explanation_receive = request.form["explanation_give"]
    mbti_receive = request.form["mbti_give"]
    url_receive = request.form["url_give"]
    comment_receive = request.form["comment_give"]

    # today = datetime.now()
    # mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    # filename = f'file-{mytime}'
    # extension = img_receive.filename.split('.')[-1]
    # save_to = f'static/{filename}.{extension}'
    # img_receive.save(save_to)
    img_file = fs.put(img_receive, filename=img_receive.filename)

    doc = {
        'picture': img_file,
        'name': name_receive,
        'intro': explanation_receive,
        'mbti': mbti_receive,
        'blog': url_receive,
        'good': comment_receive
    }
    db.introduce.insert_one(doc)

    return jsonify({'msg': '업로드 완료!'})

@app.route("/intro", methods=["GET"])
def intro_get():

    all_members = list(db.introduce.find({},{'_id':False}))   

    for member in all_members:
        image_id = member['picture']
        if image_id:
            try:
                image_data = fs.get(image_id).read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                member['picture'] = 'data:image/jpeg;base64,' + base64_image    ## 'data ....' 이 부분을 앞에 넣어줘야 img에 url로 사용 가능
            except gridfs.errors.NoFile as e:
                print("사진이 존재하지 않습니다.")    

    return jsonify({'result': all_members})

@app.route('/intro/input')
def introInput():
    return render_template('popup.html')

@app.route('/page', methods=['DELETE'])
def deletePage():
    blogurl = request.args["blogurl"]
    db.introduce.delete_one({'blog' : blogurl})
    return jsonify({'message': "삭제완료"})

@app.route('/introDetail/<name>', methods=['GET', 'POST'])
def introDetail(name):

    user = db.introduce.find_one({'name': name})

    image_id = user['picture']
    if image_id:
        try:
            image_data = fs.get(image_id).read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            user['picture'] = 'data:image/jpeg;base64,' + base64_image    ## 'data ....' 이 부분을 앞에 넣어줘야 img에 url로 사용 가능
        except gridfs.errors.NoFile as e:
            print("사진이 존재하지 않습니다.")  

    return render_template('detail.html', temp=user)

@app.route('/introTeam/<name>', methods=['GET', 'POST'])
def introTeam(name):

    user = db.introduce.find_one({'name': name})

    image_id = user['picture']
    if image_id:
        try:
            image_data = fs.get(image_id).read()
            base64_image = base64.b64encode(image_data).decode('utf-8')
            user['picture'] = 'data:image/jpeg;base64,' + base64_image    ## 'data ....' 이 부분을 앞에 넣어줘야 img에 url로 사용 가능
        except gridfs.errors.NoFile as e:
            print("사진이 존재하지 않습니다.")  

    return render_template('hello.html', temp=user)

@app.route('/introUpdate', methods=['GET', 'POST'])
def introUpdate():

    blogurl = request.args["blogurl"]

    user = db.introduce.find_one({'blog': blogurl})

    return render_template('update.html', temp=user)

@app.route("/introEdit/<name>", methods=["POST"])
def intro_update(name):

    img_receive = request.files['img_give']
    name_receive = request.form['name_give']
    explanation_receive = request.form['explanation_give']
    mbti_receive = request.form['mbti_give']
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']

    img_file = fs.put(img_receive, filename=img_receive.filename)

    db.introduce.update_one(
        {'name': name},
        {'$set':{
            'picture': img_file,
            'name': name_receive,
            'intro': explanation_receive,
            'mbti': mbti_receive,
            'blog': url_receive,
            'good': comment_receive
            }
        }
    )        
        
    return jsonify({'msg':'저장 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)