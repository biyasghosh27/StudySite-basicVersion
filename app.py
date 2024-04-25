import os
import datetime
import cv2
from flask import Flask,jsonify,request,render_template

#then install flask and face_recognition

import face_recognition

app = Flask(__name__)

#creating variable register
registered_data = {}

@app.route("/")
def index():
    #rendering html file here
    return render_template("index.html")

#creating post method
@app.route("/register",methods=["POST"])
def register():
    #request retrives value from form, json, specific URL parameters
    name = request.form.get("name")
    #uploading photos
    photo = request.files['photo']
    
    #then saving photo to uploads folder when clicks 'register'
    uploads_folder = os.path.join(os.getcwd(),"static","uploads")
    #if folder not exists auto creating folder
    if not os.path.exists(uploads_folder):
        os.makedir(uploads_folder) 

    # saving image with file name and date
    photo.save(os.path.join(uploads_folder, f'{datetime.date.today()}_{name}.jpg'))
    registered_data[name] = f'{datetime.date.today()}_{name}.jpg'

    #sending success respond then page refresh and login
    response = {"success":True,'name':name}
    #converting python data structure into json format to send them as response in API endpoints
    return jsonify(response)
    
#creating login route post
@app.route("/login", methods=["POST"])
def login():
    
    photo = request.files['photo']

    #saving photo logins to uploads folder
    uploads_folder = os.path.join(os.getcwd(),"static","uploads")
    #if folder not found creating folder
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)

    #saving photo with name
    login_filename = os.path.join(uploads_folder,"login_face.jpg")
    photo.save(login_filename)

    #in camera there is face or not
    login_image = cv2.imread(login_filename)
    gray_image = cv2.cvtColor(login_image,cv2.COLOR_BGR2GRAY)

     #now loading haar cascade file
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray_image,scaleFactor=1.1, minNeighbors=5, minSize=(30,30))

    #when no face detected
    if len(faces) == 0:
        response = {"success": False, "message": "No face detected in image."}
        return jsonify(response)
    
    login_image = face_recognition.load_image_file(login_filename)
    #processing face recognition
    #if similar then login success
    login_face_encodings = face_recognition.face_encodings(login_image)

    print("Number of face encodings in login image:", len(login_face_encodings))
    #process login photo with diff photo after register
    for name, filename in registered_data.items():
        #find registered photo in uploads folder
        registered_photo = os.path.join(uploads_folder,filename) 
        registered_image = face_recognition.load_image_file(registered_photo)
        
        # Process face recognition for the registered face
        registered_face_encodings = face_recognition.face_encodings(registered_image)

        print("Number of face encodings in registered image:", len(registered_face_encodings))

        #compare two images
        if len(registered_face_encodings) > 0 and len(login_face_encodings) > 0:
            matches = face_recognition.compare_faces(registered_face_encodings,login_face_encodings[0])

            #and see matches
            print("Matches:", matches)
            
            if any(matches):
                response =  {"success":True,"name":name}
                return jsonify(response)
  
    #when match not found
    response = {"success":False, "message": "No match found in login image."}
    return jsonify(response)

#page notification shows success
@app.route("/success")
def success():
    user_name = request.args.get("user_name")
    return render_template("parallax.html",user_name=user_name)

#creating route and function for all the html pages in the site

#login
@app.route("/index2")
def index2():
    return render_template("index2.html")
#about
@app.route("/about")
def about():
    return render_template("about.html")
#contact
@app.route("/contact")
def contact():
    return render_template("contact.html")
#course
@app.route("/course")
def course():
    return render_template("course.html") 

# to debug the code when running
if __name__ == "__main__":
    app.run(debug=True)



