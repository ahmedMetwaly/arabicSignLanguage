#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pickle
from flask_socketio import SocketIO, emit
import numpy as np
from flask import Flask, render_template
import pandas as pd
import threading



# In[2]:



app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = 'somethingsoamazingomg!!!'
socketio = SocketIO(app)


def isInitialized(hand):
    try:
        if hand.IsInitialized() == True:
            return True
    except:
        return False


with open('signs4.pkl', 'rb') as f:
    model = pickle.load(f)


# In[3]:



@app.route('/')
def home():
    return render_template('index.html')


# In[4]:

mostAppearence = []

@socketio.on('upload') 
def predict(landmarks):
    emit("speak", 'predict function called')
 
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
    className()



def most_frequent(List):
    return max(set(List), key = List.count)


def className():
    threading.Timer(5.0, className).start()
    ClassName = most_frequent(mostAppearence)
    mostAppearence.clear()
    emit("speak", str(className))
    print(ClassName)    

    





if __name__ == "__main__":
    app.config["DEBUG"] = True
    socketio.run(app)


# In[ ]:




