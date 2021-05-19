#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pickle
from flask_socketio import SocketIO, emit
import numpy as np
from flask import Flask, render_template
import pandas as pd
from playsound import playsound
from gtts import gTTS
import os
import time

# In[2]:



app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'somethingsoamazingomg!!!'
socketio = SocketIO(app)



def converter(sign):
    if sign=='wahed':
        return 'واحد'
    elif sign=='etnyn':
        return 'أثنين' 
    elif sign=='tlata':
        return 'ثلاثة' 
    elif sign=='arb3a':
        return 'أربعة'                
    elif sign=='5msa':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/yarb.mp3?alt=media&token=d6fb0837-63d5-411d-b199-d174b7639405' 
    elif sign=='sta':
        return 'ستة' 
    elif sign=='sb3a':
        return 'سبعة' 
    elif sign=='tmnya':
        return 'ثمانية' 
    elif sign=='ts3a':
        return 'تسعة' 
    elif sign=='34ra':
        return 'عشرة' 
    elif sign=='ahln':
        return 'اهلا' 
    elif sign=='esmk':
        return 'اسمك'     
    elif sign=='eyh':
        return 'ايه' 
    elif sign=='el3nwan':
        return 'العنوان'
    elif sign=='nt3rf':
        return 'نتعرف'      
    elif sign=='3aml':
        return 'عامل' 
    elif sign=='kwys':
        return 'كويس' 
    else : return 'لا استطيع فهمك'     



def most_frequent(List):
    counter = 0
    num = List[0]
      
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
  
    return num


def className():
    ClassName = most_frequent(mostAppearence)
    #SpeakSign(converter(ClassName))
    emit('voice',converter(ClassName))
    mostAppearence.clear()

    print(ClassName)    

    



with open('signs4.pkl', 'rb') as f:
    model = pickle.load(f)


# In[3]:



@app.route('/')
def home():
    return render_template('index.html')


#@socketio.on('talk')
#def SpeakSign(sign):
 #   mySign = gTTS(text=sign, lang='ar', slow=False)
  #  mySign.save("sign.mp3")
  #  playsound("sign.mp3")
   # os.remove("sign.mp3")



#@socketio.on('play')
#def Play(audio):
 #   playsound(audio)


# In[4]:

mostAppearence = []
counter =0 

@socketio.on('upload') 
def predict(landmarks):
    global counter
    #pose coordinates
    pose = landmarks['_pose']
    pose_row = list(np.array(
        [ [landmark['x'], landmark['y'], landmark['z'], landmark['visibility'] ] for landmark in pose]).flatten())
    
    #left hand coordinates
    left_hand = landmarks['_leftHand']
    left_hand_row = list(np.array(
        [ [landmark['x'], landmark['y'], landmark['z'], 0 ] for landmark in left_hand]).flatten())
   

    # right hand coordinates
    right_hand = landmarks['_rightHand']
    right_hand_row = list(np.array(
        [ [landmark['x'], landmark['y'], landmark['z'], 0 ] for landmark in right_hand]).flatten())

    rowRLH = pose_row+right_hand_row+left_hand_row
    # Make Detections
    X = pd.DataFrame([rowRLH])
    body_language_class = model.predict(X)[0]
    mostAppearence.append(body_language_class)
    #body_language_prob = model.predict_proba(X)[0]
    print(body_language_class)
    counter=counter+1
    if counter==30:
        counter=0
        className()
        time.sleep(5)

    







if __name__ == "__main__":
    app.config["DEBUG"] = False
    socketio.run(app,ssl_context="adhoc")


# In[ ]:




