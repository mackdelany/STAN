var AirwayObservation = false;
$("input[name='airway']").on("change", function(e){
    AirwayObservation = true;
});

var BreathingObservation = false;
$("input[name='breathing']").on("change", function(e){
    BreathingObservation = true;
});

var CirculatorySkinObservation = false;
$("input[name='circulation']").on("change", function(e){
    CirculatorySkinObservation = true;
});

var NeurovascObservation = false;
$("input[name='neurovasc']").on("change", function(e){
    NeurovascObservation = true;
});

var ImmunocompromisedObservation = false;
$("input[name='immunocompromised']").on("change", function(e){
    ImmunocompromisedObservation = true;
});

var MentalHealthObservation = false;
$("input[name='mentalhealth']").on("change", function(e){
    MentalHealthObservation = true;
});


var PainScaleObservation = false;
var DisabilityValueObservation = false;
var VitalSignsPulseObservation = false;
var RespiratoryRateObservation = false;
var BloodPressureObservation = false;
var TemperatureObservation = false;
var SatsObservation = false;


function observePainScale(){
    PainScaleObservation = true;
};

function observeDisabilityValue(){
    DisabilityValueObservation = true;
};

function observeVitalSignsPulse(){
    VitalSignsPulseObservation = true;
};

function observeRespiratoryRate(){
    RespiratoryRateObservation = true;
};

function observeBloodPressure(){
    BloodPressureObservation = true;
};

function observeTemperature(){
    TemperatureObservation = true;
};

function observeSats(){
    SatsObservation = true;
};

function refreshPage(){
    window.location.reload();
} 


