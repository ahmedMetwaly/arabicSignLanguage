// socketio initialization
//<script type="module">


var Pcounter = 0;
var Lcounter = 0;
var Rcounter = 0;

const socket = io();
const synth = window.speechSynthesis;


socket.on('speak', function(message){
    const msg = new SpeechSynthesisUtterance(message);
    synth.speak(msg);
})


socket.on('prediction', function (_pose,_leftHand,_rightHand) {
    socket.emit('upload',_pose,_leftHand,_rightHand)
  
}); 



const videoElement = document.getElementsByClassName('input_video')[0];
const canvasElement = document.getElementsByClassName('output_canvas')[0];
const canvasCtx = canvasElement.getContext('2d');

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
              
  
  if(results.leftHandLandmarks==undefined){
      //Lcounter++;
      //if(Lcounter==15){
        //emit('speak','move back to detect left hand')
        //Lcounter=0;
      //}
      console.log("left hand is Not intialized");

  }

  if(results.rightHandLandmarks==undefined){
      //Rcounter++;
      //if(Rcounter==15){
        //emit('speak','move back to detect right hand')
        //Rcounter=0;
      //}
    console.log("right hand is Not intialized");

  }
  if(results.poseLandmarks==undefined){
     // Pcounter++;
      //if(Pcounter==15){
        //emit('speak','move back to detect your pones')
        //Pcounter=0;
      //}

    console.log("pose is Not intialized");

  }

  if(results.poseLandmarks!=undefined && results.rightHandLandmarks!=undefined && results.leftHandLandmarks!=undefined){
    
    console.log('before prediction')
    socket.emit('upload',results.poseLandmarks,results.leftHandLandmarks,results.rightHandLandmarks)
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



