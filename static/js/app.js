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


socket.on('voice', function(voice){
  document.getElementById("audio").setAttribute('src',voice );
  audio.play(); //
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
              
  
  //if(results.leftHandLandmarks==undefined){
    //  Lcounter++;
      //if(Lcounter==30){
        //socket.emit('play','moveBack.mp3')
        //Lcounter=0;
        //Stop = false
      //}
      //console.log("left hand is Not intialized");
  //}

  if(results.rightHandLandmarks==undefined || results.leftHandLandmarks==undefined || results.poseLandmarks==undefined){
      Rcounter++;
      if(Rcounter==90){
        
        //socket.emit('play','من فضلك ارجع خطوة للخلف')
        Rcounter=0
        Stop = false

      }
    console.log("right hand is Not intialized");

  }
  //if(results.poseLandmarks==undefined){
    // Pcounter++;
      //if(Pcounter==60){
        //socket.emit('play','moveBack.mp3')
        //Pcounter=0
        //Stop = false
      //}

    //console.log("pose is Not intialized");
  //}

  if(results.poseLandmarks!=undefined && results.rightHandLandmarks!=undefined && results.leftHandLandmarks!=undefined){
    Pcounter++;
    if(Pcounter==30){
     //socket.emit('play','start.mp3')
      Pcounter=0
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



