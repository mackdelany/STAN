function triageRulesExist(triageRules){

    for (var key in triageRules){

        if (triageRules[key].length > 0){

            return true
        }
    }
    return false
}


function triageRuleTable(triageRules){

    const tablearea = document.getElementById('triage-rule-table-div');

    while (tablearea.firstChild) {
        tablearea.removeChild(tablearea.firstChild);
      }

    if (triageRulesExist(triageRules)){

        const table = document.createElement("table");
        table.id = "triage-rule-table";

        const triageCodeTitle = document.createTextNode('Triage code');
        const triageRuleTitle = document.createTextNode('Relevant indicators');
        
        const title_row = table.insertRow(0);
    
        const code_title_cell = title_row.insertCell(0);
        const rule_title_cell = title_row.insertCell(1);

        code_title_cell.className = 'triage-table-header';
        rule_title_cell.className = 'triage-table-header';
    
        code_title_cell.append(triageCodeTitle);
        rule_title_cell.append(triageRuleTitle);
    
        for (var key in triageRules) {
    
            if (triageRules[key].length > 0) {
    
                let row = table.insertRow(-1);
    
                let code_cell = row.insertCell(0);
                let rule_cell = row.insertCell(1);

                code_cell.className = ('triage-table-code-cell')
                rule_cell.className = ('triage-table-rule-cell')
    
                let triageCode = document.createTextNode(key.charAt(key.length - 1));
    
                code_cell.append(triageCode);

                let rule_insert = 0
    
                for (let rule in triageRules[key]){
    
                    let triageRule = document.createTextNode(triageRules[key][rule]);
                    let br1 = document.createElement('br');
                    let br2 = document.createElement('br');
    
                    if (rule_insert > 0){rule_cell.append(br1)};
                    rule_cell.append(triageRule);
                    rule_cell.append(br2);

                    rule_insert ++ ;
                }
            }
        }

        tablearea.appendChild(table);

    }

}

