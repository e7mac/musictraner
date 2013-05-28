//metronome code
metronome = function(withTempo,withSound,withContext) {
    var that = {};
    
    //private variables
    var tempo = withTempo;
    var sound = withSound;
    var context = withContext;

    var isPlaying = false;
    var intervalID;

    that.getSound = function () {
        return sound;
    }

    
    that.getIsPlaying = function () {
        return isPlaying;
    }
    
    
    that.toggleMetronome = function() {
        if (isPlaying === true) {
            that.stopMetronome();
        }
        else {
            that.startMetronome();
        }
    }
    
    that.setTempo = function(newTempo) {
        //console.log('set');
        tempo = newTempo;
        if (isPlaying === true) {
            //console.log('refresh');
            that.stopMetronome();
            that.startMetronome();        
        }
    }

    that.loadSound = function () {
        var request = new XMLHttpRequest();
        request.open('GET', sound, true);
        request.responseType = 'arraybuffer';
        // Decode asynchronously
        request.onload = function() {
            context.decodeAudioData(request.response, function(buff) {sound = buff;}, onError);
        }
        request.send();        
    }

    that.playSound = function () {
        var source = context.createBufferSource(); // creates a sound source
        source.buffer = sound;                    // tell the source which sound to play
        source.connect(context.destination);       // connect the source to the context's destination (the speakers)
        source.noteOn(0);                          // play the source now
    }

    that.getTempo = function() {
        //console.log(tempo);
        return tempo;
    }

    that.startMetronome = function() {
        isPlaying = true;
        intervalID = setInterval(function () {that.playSound();},1000/tempo*60);
    }
    
    that.stopMetronome = function() {
        //console.log('stop');
        isPlaying = false;
        clearInterval(intervalID);
    }
    return that;
};

context = new webkitAudioContext();
onError = function (err) {
}