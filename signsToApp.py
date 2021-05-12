#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import cv2
import pickle
from flask_socketio import SocketIO, emit, send
import numpy as np
from flask import Flask, request, jsonify, render_template, send_from_directory
from sklearn.metrics import accuracy_score  # Accuracy metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import pandas as pd
import csv


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


@socketio.on('upload')
def predict(_pose,_leftHand,_rightHand):
    print('i was here')
     # Extract Pose landmarks
    if isInitialized(_pose) == False:
        emit("speak", 'move back to appear')

    # Extract left_hand landmarks
    if isInitialized(_leftHand) == False:
        emit("speak", "move back one step to detect left hand")

    # Exract right_hand landmarks
    if isInitialized(_rightHand) == False:
        emit("speak", "move back one step to detect right hand")
    # Concate rows
    # pose detection
    pose = _pose
    pose_row = list(np.array(
        [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
    # left hand coordinates
    left_hand = _leftHand
    left_hand_row = list(np.array(
        [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in left_hand]).flatten())

    # right hand coordinates
    right_hand = _rightHand
    right_hand_row = list(np.array(
        [[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in right_hand]).flatten())

    rowRLH = pose_row+right_hand_row+left_hand_row
    # Make Detections
    X = pd.DataFrame([rowRLH])
    body_language_class = model.predict(X)[0]
    #body_language_prob = model.predict_proba(X)[0]
    print(body_language_class)
    emit("speak", body_language_class)



if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




