function makePayload(method = 'PREDICT-TESTING') {

    var today = new Date();
    const payload = {
                    "Hospital": "index.html",
                    "DHB": "index.html",
                    "DOB": ((
                        today.getFullYear() - Age) + "-" + 
                        (today.getMonth() + 1) + "-1 00:00:00.000"
                        ), 
                    "Gender": d3.select('input[name="gender"]:checked').property("value"), 
                    "PresentingComplaint": PresentingComplaint, 
                    "PresentDateTime": ((
                        today.getFullYear()) + "-" + 
                        (today.getMonth() + 1) + "-" + 
                        (today.getDate()) + " " + 
                        today.getHours() + ":" + 
                        today.getMinutes() + ":00.000"
                        ),
                    "Method": method
                };

    if (AirwayObservation){
        payload["Airway"] = d3.select('input[name="airway"]:checked').property("value") ;
    }

    if (BreathingObservation){
        payload["Breathing"] = d3.select('input[name="breathing"]:checked').property("value") ;
    }

    if (CirculatorySkinObservation){
        payload["CirculatorySkin"] = d3.select('input[name="circulation"]:checked').property("value") ;
    }

    if (NeurovascObservation){
        payload["NeuroAssessment"] = d3.select('input[name="neurovasc"]:checked').property("value") ;
    }

    if (ImmunocompromisedObservation){
        payload["Immunocompromised"] = +d3.select('input[name="immunocompromised"]:checked').property("value") ;
    }

    if (MentalHealthObservation){
        payload["MentalHealthConcerns"] = d3.select('input[name="mentalhealth"]:checked').property("value") ;
    }

    if (PainScaleObservation){
        payload["PainScale"] = sliderPain.value() ;
    }

    if (DisabilityValueObservation){
        payload["DisabilityValue"] = disabilitySubmission[sliderDisability.value()] ;
    }

    if (VitalSignsPulseObservation){
        payload["VitalSignsPulse"] = sliderVitalsigns.value() ;
    }

    if (RespiratoryRateObservation){
        payload["RespiratoryRate"] = sliderRespiratory.value() ;
    }

    if (BloodPressureObservation){
        payload["BloodPressure"] = sliderBloodPressureSystolic.value() + '/' + sliderBloodPressureDiastolic.value();
    }

    if (TemperatureObservation){
        payload["Temperature"] = sliderTemperature.value() ;
    }

    if (SatsObservation){
        payload["Sats"] = sliderSats.value() ;
    }

    payload["TriageAssessment"] = document.getElementById("triage-assessment").value

    return payload

}