function renderCodeAndEws(triage_code_div_id, triage_code, ews_message){

    const triage_code_div = document.getElementById(triage_code_div_id);

    let triage_code_text_node = document.createElement('p');
    let triage_code_text = document.createTextNode("Predicted triage code");
    triage_code_text_node.style.fontWeight = 'bold';
    triage_code_text_node.appendChild(triage_code_text);
    triage_code_div.appendChild(triage_code_text_node);

    let inner_number_div = document.createElement("div");
    inner_number_div.id = 'triage-code-number';

    let triage_code_number_node = document.createElement('h1');
    let triage_code_number = document.createTextNode(triage_code);
    triage_code_number_node.appendChild(triage_code_number);
    inner_number_div.appendChild(triage_code_number_node);
    //inner_number_div.style.margin = '10px';;
    //inner_number_div.style.padding = '1px';;

    if (triage_code > 4.25){
        inner_number_div.style.backgroundColor = "#a65628";
    }
    else if (triage_code > 3.5){
        inner_number_div.style.backgroundColor = "#377eb8";
    }
    else if (triage_code > 2.5){
        inner_number_div.style.backgroundColor = "#69b3a2";
    }
    else if (triage_code > 1.75){
        inner_number_div.style.backgroundColor = "#ff7f00";
    }
    else if (triage_code < 1.76){
        inner_number_div.style.backgroundColor = "#e41a1c";
    };

    triage_code_div.appendChild(inner_number_div);

    if (ews_message != "Not enough data for EWS estimate."){
        let ews_message_node = document.createElement('p');
        let ews_message_text = document.createTextNode(ews_message);
        ews_message_node.appendChild(ews_message_text);
        triage_code_div.appendChild(ews_message_node);
    };
};