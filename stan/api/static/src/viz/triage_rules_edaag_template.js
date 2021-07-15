/*
 * triagerules.js
 * 2020 STAN
 *
 * This function is used to parse and render relevant triage rules.
 * 
 */


function triageRulesExist(triageRules) {

    for (var key in triageRules) {

        if (triageRules[key].length > 0) {

            return true
        }
    }
    return false
};

function triageRuleTableEdaag(triageRules) {

    const tablearea = document.getElementById('triage-rules-template');

    while (tablearea.firstChild) {
        tablearea.removeChild(tablearea.firstChild);
    }

    if (triageRulesExist(triageRules)) {

        const table = document.createElement("table");
        table.id = "triage-rules-table-template";

        const triageCode1 = document.createTextNode('1');
        const triageCode2 = document.createTextNode('2');
        const triageCode3 = document.createTextNode('3');
        const triageCode4 = document.createTextNode('4');
        const triageCode5 = document.createTextNode('5');
        
        const title_row = table.insertRow(0);

        const code_1_cell = title_row.insertCell(0);
        const code_2_cell = title_row.insertCell(1);
        const code_3_cell = title_row.insertCell(2);
        const code_4_cell = title_row.insertCell(3);
        const code_5_cell = title_row.insertCell(4);

        code_1_cell.className = 'triage-header-1';
        code_2_cell.className = 'triage-header-2';
        code_3_cell.className = 'triage-header-3';
        code_4_cell.className = 'triage-header-4';
        code_5_cell.className = 'triage-header-5';

        code_1_cell.append(triageCode1);
        code_2_cell.append(triageCode2);
        code_3_cell.append(triageCode3);
        code_4_cell.append(triageCode4);
        code_5_cell.append(triageCode5);

        let row = table.insertRow(-1);
        let cell_insert = 0;
      
        for (var key in triageRules) {

            let rule_cell = row.insertCell(cell_insert);

            rule_cell.className = ('triage-table-rule-cell-template')

            if (triageRules[key].length > 0) {

                let rule_insert = 0;

                for (let rule in triageRules[key]) {

                    let triageRule = document.createTextNode(triageRules[key][rule]);
                    let br1 = document.createElement('br');
                    let br2 = document.createElement('br');

                    if (rule_insert > 0) { rule_cell.append(br1) };
                    rule_cell.append(triageRule);
                    rule_cell.append(br2);

                    rule_insert++;
                }
            }
            cell_insert++;
        }

        tablearea.appendChild(table);

    }

}

