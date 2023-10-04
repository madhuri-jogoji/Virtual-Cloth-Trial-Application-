from flask import Flask,render_template,Response,request,redirect,session
import cv2
import os

import cvzone
import mysql.connector

from cvzone.PoseModule import PoseDetector


#globalling declaring web capture
global stop_webcam,id,users
stop_webcam=False


main = Flask(__name__)
main.secret_key=os.urandom(24)



def TryOn(clothNum=0,gen='boy',cat="round",stop_web=False):
    if gen=='girl':
        if cat=="collor":
            listShirts = os.listdir("resources/G_collor")
        else:
            if cat=="round":
                listShirts = os.listdir("resources/G_round")
    elif gen=='boy':
        if cat=="collor":
            listShirts = os.listdir("resources/B_collor")
        elif cat=="round":
            listShirts = os.listdir("resources/B_round")
        else:
            if cat=="formal":
                listShirts = os.listdir("resources/B_formal")
        
       
             
        

    cap = cv2.VideoCapture(0)
    detector = PoseDetector()
    
    print(listShirts)

    fixedRatioW=270/200 #widthOfShirt/widthOfPoint11to12
    # fixedRatioH=286/280
    shirtWidth=750
    shirtHeight=895
    shirtRatioHeightWidth=shirtHeight/shirtWidth
    
    clothButtonLeft=cv2.imread("resources/button.png",cv2.IMREAD_UNCHANGED)
    clothButtonRight=cv2.flip(clothButtonLeft,1)
    counterRight=0
    counterLeft=0
    selectionSpeed=10
    

    while True:

        if stop_webcam:
            break
        success, img = cap.read()


        img = detector.findPose(img,draw=False)
        #img=cv2.flip(img,1)
        lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False)
        if lmList:
            # center = bboxInfo["center"]
            # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
            lm11=lmList[11][1:3]
            lm12=lmList[12][1:3]
            lm26=lmList[26][1:3]
            print(lm26)
            if gen=='girl' and cat=="collor":
                imgShirt = cv2.imread(os.path.join("resources/G_collor", listShirts[clothNum]), cv2.IMREAD_UNCHANGED)
            elif gen=='girl' and cat=="round":
                imgShirt = cv2.imread(os.path.join("resources/G_round", listShirts[clothNum]), cv2.IMREAD_UNCHANGED)
            elif gen=='boy' and cat=="collor":
                imgShirt = cv2.imread(os.path.join("resources/B_collor", listShirts[clothNum]), cv2.IMREAD_UNCHANGED)
            elif gen=='boy' and cat=="round":
                imgShirt = cv2.imread(os.path.join("resources/B_round", listShirts[clothNum]), cv2.IMREAD_UNCHANGED)
            elif gen=='boy' and cat=="formal":
                imgShirt = cv2.imread(os.path.join("resources/B_formal", listShirts[clothNum]), cv2.IMREAD_UNCHANGED)


            widthOfShirt=int((lm11[0]-lm12[0])*fixedRatioW)
            # heightOfShirt=int((lm26[0]-lm12[0])*fixedRatioH)
            print(widthOfShirt)
            imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shirtRatioHeightWidth)))
            # imgShirt = cv2.resize(imgShirt, (heightOfShirt, int(heightOfShirt * shirtRatioHeightWidth)))

            currentScale=int(lm11[0]-lm12[0])/190
            offset=int(44*currentScale),int(48*currentScale)


            try:

                img = cvzone.overlayPNG(img, imgShirt,(lm12[0]-offset[0],lm12[1]-offset[1]))
            except:
                pass

            img=cvzone.overlayPNG(img,clothButtonLeft,(12,200))
            img=cvzone.overlayPNG(img,clothButtonRight,(530,200))

            if lmList[16][1]<100:
                counterLeft+=1
                cv2.ellipse(img,(55,245),(38,38),0,0,counterLeft*selectionSpeed,(0,255,0),15)

                if counterLeft*selectionSpeed>360:
                    counterLeft=0
                    if clothNum<len(listShirts)-1:
                        clothNum+=1


            elif lmList[15][1]>500:
                counterRight += 1
                cv2.ellipse(img, (575, 245), (38, 38), 0, 0, counterRight * selectionSpeed, (0, 255, 0), 15)

                if counterRight * selectionSpeed > 360:
                    counterRight = 0
                    if clothNum > 0:
                        clothNum -= 1


            else:
                counterRight=0
                counterLeft=0
             
            ret, jpeg = cv2.imencode('.jpg', img)

            frame = jpeg.tobytes()
        
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # buffer=cv2.imencode('.jpg',img)
        # frame=buffer.tobytes()
        # cv2.imshow("Image", img)
        # cv2.waitKey(1)
        # yield(b'--frame\r\n'b'Content-Type:video\r\n\r\n'+img+b'\r\n')

    # while True:
    #     success,frame=camera.read()
    #     if not success:
    #         break
    #     else:
    #         ret,buffer=cv2.imencode('.jpg',frame)
    #         frame=buffer.tobytes()
    #     yield(b'--frame\r\n'b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')







@main.route("/")
def home():
    if 'id' not in session:
        return render_template("front.html")
    else:
        return redirect('/index')

    

@main.route("/index")
def index():
    if 'id' in session:
        return render_template("index.html")
    else:
        return redirect('/')

    


@main.route("/about")
def about():
    return render_template("about.html")


@main.route("/video")
def video():
    return render_template("video.html")




@main.route("/video0")
def video0():
    clothNum=0
    gen='boy'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video1")
def video1():
    clothNum=1
    gen='boy'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video2")
def video2():
    clothNum=2
    gen='boy'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video3")
def video3():
    clothNum=0
    gen='boy'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video4")
def video4():
    clothNum=1
    gen='boy'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')


@main.route("/video5")
def video5():
    clothNum=2
    gen='boy'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video6")
def video6():
    clothNum=3
    gen='boy'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video7")
def video7():
    clothNum=4
    gen='boy'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video8")
def video8():
    clothNum=0
    gen='boy'
    cat="formal"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video9")
def video9():
    clothNum=1
    gen='boy'
    cat="formal"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video10")
def video10():
    clothNum=0
    gen='girl'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')


@main.route("/video11")
def video11():
    clothNum=1
    gen='girl'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video12")
def video12():
    clothNum=2
    gen='girl'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video13")
def video13():
    clothNum=3
    gen='girl'
    cat="collor"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video14")
def video14():
    clothNum=0
    gen='girl'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video15")
def video15():
    clothNum=1
    gen='girl'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')

@main.route("/video16")
def video16():
    clothNum=2
    gen='girl'
    cat="round"
    stop_webcam=False
    return Response(TryOn(clothNum,gen,cat,stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')



# @main.route("/video")
# def video():
    
#     return cap
    

# @main.route("/videoWeb")
# def videoWeb():
#     return Response(video5(),mimetype='multipart/x-mixed-replace; boundary=frame')

# def fun1(res):
#     return res


# def stop_webcam():
#     global stop_webcam
#     stop_webcam = True

# @main.route('/stop-webcam')
# def stop():
#     stop_webcam=True
#     return Response(generate_frames(stop_webcam),mimetype='multipart/x-mixed-replace;boundary=frame')


@main.route("/B_collor")
def B_collor():
    return render_template("B_collor.html")

@main.route("/B_round")
def B_round():
    return render_template("B_round.html")

@main.route("/B_formal")
def B_formal():
    return render_template("B_formal.html")

@main.route("/G_collor")
def G_collor():
    return render_template("G_collor.html")

@main.route("/G_round")
def G_round():
    return render_template("G_round.html")



@main.route("/girl")
def girl():
    return render_template("girls.html")

@main.route("/boy")
def boy():
    return render_template("boys.html")



# database connection for authentication
con=mysql.connector.connect(host='127.0.0.1',user='root',password='madhuri09',database='tryon')
cursor=con.cursor()

@main.route('/login_validation',methods=['POST'])
def login_validation():
    username=request.form.get('username')
    password=request.form.get('password')
    cursor.execute("select *from users WHERE username = %s AND password = %s " ,(username,password))

    users = cursor.fetchall()
    if len(users)>0:
        session['id']=users[0][0]
        return redirect('/index')
    else:

        return redirect('/') 
    
@main.route("/add_user",methods=['POST'])
def add_user():
    username=request.form.get('rusername')
    password=request.form.get('rpassword')
    email=request.form.get('remail')
    cursor.execute("INSERT INTO users (username,password,email) VALUES(%s,%s,%s)",(username,password,email))
    con.commit()
    

    cursor.execute("select *from users WHERE email = %s ",[email])
    myuser=cursor.fetchall()
    session['id']=myuser[0][0]
    return redirect('/index')
    
    
        
        


@main.route('/logout')
def logout():
    session.pop('id')
    return redirect('/')
    

@main.route('/offline.html')
def offline():
    return main.send_static_file('offline.html')


@main.route('/service-worker.js')
def sw():
    return main.send_static_file('service-worker.js')

if __name__ == '__main__':
    main.run(host="0.0.0.0",port=8080, debug=True)

    # Serve the app with gevent
    # http_server = WSGIServer(('', 4050), app)
    # http_server.serve_forever()
    main.run()

# if __name__=="__main__":

#     main.run(debug=True,port=5000)

