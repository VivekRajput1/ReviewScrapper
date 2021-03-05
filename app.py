# doing necessary imports

from flask import Flask, render_template, request,jsonify
# from flask_cors import CORS,cross_origin
import  flipkart
import  db


app = Flask(__name__)  # initialising the flask app with the name 'app'

@app.route('/',methods=['POST','GET']) # route with allowed methods as POST and GET
def index():
    if request.method == 'POST':
        searchString = request.form['content'].replace(" ","") # obtaining the search string entered in the form
        try:
            reviews = db.getDataFromMongo(searchString) # searching the collection with the name same as the keyword
            if reviews.count() >= 10: # if there is a collection with searched keyword and it has records in it
                return render_template('results.html',reviews=reviews) # show the results to user
            else:
                data=flipkart.getDataFromFlipKart(searchString)
                db.SaveDatainMongo(searchString,data)
                reviews = db.getDataFromMongo(searchString)
                return render_template('results.html', reviews=reviews) # showing the review to the user
        except Exception as e:
            return e
            #return render_template('results.html')
    else:
        return render_template('index.html')
if __name__ == "__main__":
    app.run(port=8000,debug=True) # running the app on the local machine on port 8000
