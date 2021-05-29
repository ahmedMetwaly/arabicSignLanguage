#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pickle
from flask_socketio import SocketIO, emit
import numpy as np
from flask import Flask, render_template
import pandas as pd
import time
from zipfile import ZipFile


# In[2]:



app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'somethingsoamazingomg!!!'
socketio = SocketIO(app)



def converter(sign):
    if sign=='wahed':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D9%88%D8%A7%D8%AD%D8%AF.mp3?alt=media&token=fa089356-b7f6-412c-9538-9d379a7fa06d'
    elif sign=='etnyn':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D8%AB%D9%86%D9%8A%D9%86.mp3?alt=media&token=45013b81-5275-410e-aabc-42aabe83df43' 
    elif sign=='tlata':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%AB%D9%84%D8%A7%D8%AB%D8%A9.mp3?alt=media&token=b6a9522d-f73e-400b-a188-ac823df74b75' 
    elif sign=='arb3a':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A3%D8%B1%D8%A8%D8%B9%D8%A9.mp3?alt=media&token=c670705b-1328-4914-8599-d1fa229e73a5'                
    elif sign=='5msa':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%AE%D9%85%D8%B3%D8%A9.mp3?alt=media&token=76f6d595-3f5d-4fbc-a317-1e09723b9b14' 
    elif sign=='sta':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%B3%D8%AA%D8%A9.mp3?alt=media&token=e28aa910-579b-4db2-b84c-468fe1fc9c99' 
    elif sign=='sb3a':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%B3%D8%A8%D8%B9%D8%A9.mp3?alt=media&token=50aa62e6-63ae-4059-8b0d-828ff4d0e5ee' 
    elif sign=='tmnya':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%AB%D9%85%D8%A7%D9%86%D9%8A%D8%A9.mp3?alt=media&token=385edbc2-c46b-4ef9-bf0a-ca8b79c32d7c' 
    elif sign=='ts3a':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%AA%D8%B3%D8%B9%D8%A9.mp3?alt=media&token=8e21ec5a-4a1a-48b7-b1ae-33adfd768736' 
    elif sign=='34ra':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%B9%D8%B4%D8%B1%D8%A9.mp3?alt=media&token=00228197-7cc6-4aa1-8c02-2ef8eac1ab16' 
    elif sign=='ahlnwshln':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D9%87%D9%84%D8%A7%20%D9%88%D8%B3%D9%87%D9%84%D8%A7.mp3?alt=media&token=031d57ea-b9fc-4015-8d5b-8fb09018839b' 
    elif sign=='esmk':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D8%B3%D9%85%D9%83.mp3?alt=media&token=bb3a1f4f-0de0-4644-a514-39fa0f7e6683'     
    elif sign=='eyh':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D9%8A%D9%87.mp3?alt=media&token=f06d04e0-dade-4bee-83c0-6d513c08cc46' 
    elif sign=='el3nwan':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D9%84%D8%B9%D9%86%D9%88%D8%A7%D9%86.mp3?alt=media&token=8cad20bd-1d16-4afd-afe2-44699b5e516b'
    elif sign=='nt3rf':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D9%86%D8%AA%D8%B9%D8%B1%D9%81.mp3?alt=media&token=6240fffa-6f01-4025-88de-7122c5e00dc1'      
    elif sign=='3aml':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%B9%D8%A7%D9%85%D9%84.mp3?alt=media&token=800d9603-52ca-409a-b1ee-907a8411aa51' 
    elif sign=='kwys':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D9%83%D9%88%D9%8A%D8%B3.mp3?alt=media&token=cddbb5a8-5516-4dbc-8e14-f5eacf437199' 
    elif sign=='4krn':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%B4%D9%83%D8%B1%D8%A7.mp3?alt=media&token=40f8c9fc-312e-4922-8d62-6c215a96e6c9' 
    elif sign=='2sf':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D8%B3%D9%81.mp3?alt=media&token=9d791e8f-de44-4a03-904a-a10bb5ef9e9d'
    elif sign=='7adr':
        return 'https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%AD%D8%A7%D8%B6%D8%B1.mp3?alt=media&token=80d02f2a-964c-4b2f-91ba-908126f2330c'
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

    
    
with ZipFile('signs9.zip', 'r') as zipObj:
   # Extract all the contents of zip file in current directory
   zipObj.extractall()


with open('signs9.pkl', 'rb') as f:
    model = pickle.load(f)


# In[3]:



@app.route('/')
def home():
    return render_template('index.html')


@socketio.on('sleep')
def sleep(ms):
    time.sleep(ms)
    print('called after sleep ms')




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
        sleep(1)

    







if __name__ == "__main__":
    app.config["DEBUG"] = False
    socketio.run(app,ssl_context="adhoc")


# In[ ]:




