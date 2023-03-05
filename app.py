import boto3, botocore
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy 
import uuid
import io
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from dotenv import load_dotenv
import dotenv

load_dotenv()

app = Flask(__name__)
db = SQLAlchemy()
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpeg', 'mp4'}





def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    bucket = db.Column(db.String(100))

    
#def create_app():
 #   app = Flask(__name__)   
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    
    db.init_app(app)
#app = create_app()
@app.route("/", methods=["GET", "POST"])
def index():
         if request.method == "POST":
             uploaded_file = request.files["file-to-save"]
             if not allowed_file(uploaded_file.filename):
                return "FILE NOT ALLOWED"
        
             new_filename = uuid.uuid4().hex + '.' + uploaded_file.filename.rsplit('.',1)[1].lower()
             bucket_name ="flasks3testexample"
             s3 = boto3.resource(
        "s3",
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_ACCESS_SECRET'),
       # aws_bucket_name =os.getenv(AWS_BUCKET_NAME)
             )       
            
             
             s3.Bucket(bucket_name).upload_fileobj(uploaded_file, new_filename)
        
             file = File(filename=new_filename, bucket=bucket_name)
        
             db.session.add(file)
             db.session.commit()
        
             return redirect(url_for("index"))
    
         files = File.query.all()
    
         return render_template("index.html", files=files)
    
         #return  app


if __name__ == "__main__":
    
    app.run(host='127.0.0.1', port=5000,debug=True)

