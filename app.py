from flask import Flask,render_template,redirect,url_for,request,Response,jsonify

app=Flask(__name__)

@app.route('/query-response',methods=['POST','GET'])
def home():
    if request.method=='POST':
        query=request.form['query']
        print(query)
    return jsonify({"query entered is ":query})




if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')