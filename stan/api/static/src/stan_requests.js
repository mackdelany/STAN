var triageCodeDiv = d3.select("#triage-code-prediction");
var earlyWarningScoreDiv = d3.select("#early-warning-score");
var triageRuleDiv = d3.select("#triage-rules");

function predictOnPage(endpoint = '/predict-testing') {
    
    var payload = makePayload()

    $.ajax({
        url: endpoint,
        headers: {'Key': 'kvur93m4-n0dk-0kjf-038g-j4ll2dk4mfkg'},
        data : JSON.stringify(payload),
        type : 'POST',
        contentType : 'application/json',
        success: function( data, textStatus){
            console.log(textStatus);
            triageCodeDiv.text('Predicted Triage Code: ' + (Math.round(data.triage_code*100)/100));
            earlyWarningScoreDiv.text(data.early_warning_score.message);
            triageRuleTable(data.triage_rules);
            buildGraph(data.prediction_distribution, data.triage_code);
        }
    });
};

function templateOnPage(endpoint = 'predict-testing') {

    var payload = makePayload()
    
    $.ajax({
        url: endpoint,
        headers: {'Key': 'kvur93m4-n0dk-0kjf-038g-j4ll2dk4mfkg'},
        data : JSON.stringify(payload),
        type : 'POST',
        contentType : 'application/json',
        success: function(data, textStatus){

            stan_response = {
                "triage_code": Math.round(data.triage_code),
                "warnings": data.warnings,
                "triage_rules_1": data.triage_rules['Code1'],
                "triage_rules_2": data.triage_rules['Code2'],
                "triage_rules_3": data.triage_rules['Code3'],
                "triage_rules_4": data.triage_rules['Code4'],
                "triage_rules_5": data.triage_rules['Code5'],
                "ews_message": data.early_warning_score.message,
                "prediction_distribution": data.prediction_distribution
            };

            $("body").load("/load_edaag_template", stan_response);  // this loads great but in same browser
            
        }
    });
};


function templateNewPage(endpoint = 'predict-testing') {
    var payload = makePayload(endpoint)

    $.ajax({
        url: '_log_input_to_global',
        headers: {'Key': 'kvur93m4-n0dk-0kjf-038g-j4ll2dk4mfkg'},
        data : JSON.stringify(payload),
        type : 'POST',
        contentType : 'application/json',
        success: function(data, textStatus){
            window.open('/_super_input', '_blank')
        }
    });
};