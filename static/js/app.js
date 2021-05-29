// socketio initialization
//<script type="module">


var Pcounter = 0;
var Lcounter = 0;
var Rcounter = 0;
var Stop =false; 


const socket = io();





const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');


function voice(vc){
  var audio = document.getElementById("audio").setAttribute('src',vc );
  audio.play(); 
}


socket.on('voice', function(vc){
  voice(vc)
})





function onResults(results) {
  canvasCtx.save();
  canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
  canvasCtx.drawImage(
      results.image, 0, 0, canvasElement.width, canvasElement.height);
  drawConnectors(canvasCtx, results.poseLandmarks, POSE_CONNECTIONS,
                {color: '#00FF00', lineWidth: 4});
  drawLandmarks(canvasCtx, results.poseLandmarks,
                {color: '#FF0000', lineWidth: 2});
  drawConnectors(canvasCtx, results.faceLandmarks, FACEMESH_TESSELATION,
                {color: '#C0C0C070', lineWidth: 1});
  drawConnectors(canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS,
                {color: '#CC0000', lineWidth: 5});
  drawLandmarks(canvasCtx, results.leftHandLandmarks,
                {color: '#00FF00', lineWidth: 2});
  drawConnectors(canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS,
                {color: '#00CC00', lineWidth: 5});
  drawLandmarks(canvasCtx, results.rightHandLandmarks,
                {color: '#FF0000', lineWidth: 2});
              
  
 
  if(results.rightHandLandmarks==undefined || results.leftHandLandmarks==undefined || results.poseLandmarks==undefined){
      Rcounter++;
      if(Rcounter==90){
        Rcounter=0
        voice('https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D9%8A%D8%AF%D9%83%20%D8%BA%D9%8A%D8%B1%20%D9%88%D8%A7%D8%B6%D8%AD%D9%87.mp3?alt=media&token=50709ce5-c3aa-4cf0-bb1f-23bd2ee1dfef')
       
        Stop = false

      }
    console.log("right hand is Not intialized");

  }

  if(results.poseLandmarks!=undefined && results.rightHandLandmarks!=undefined && results.leftHandLandmarks!=undefined){
    Pcounter++;
    if(Pcounter==30){
      voice('https://firebasestorage.googleapis.com/v0/b/sign-s-voices.appspot.com/o/%D8%A7%D8%A8%D8%AF%D8%A3%D8%B9%D9%85%D9%84%20%D8%A7%D9%84%D8%A7%D8%B4%D8%A7%D8%B1%D8%A9.mp3?alt=media&token=e1636125-6106-40f9-9a1c-c82344e2945f')
    
    }
      
    
    var landmarks =   {'_pose': results.poseLandmarks,
      '_leftHand':results.leftHandLandmarks,
      '_rightHand':results.rightHandLandmarks}
    console.log('before prediction')
    socket.emit('upload',landmarks)   
    console.log('after prediction')
 
  }

  canvasCtx.restore();
}


const holistic = new Holistic({locateFile: (file) => {
  return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
}});
holistic.setOptions({
  modelComplexity: 1,
  smoothLandmarks: true,
  minDetectionConfidence: 0.5,
  minTrackingConfidence: 0.5
});
holistic.onResults(onResults);
const camera = new Camera(videoElement, {
  onFrame: async () => {
    await holistic.send({image: videoElement});
  },
  width: 1280,
  height: 720
});
camera.start();



