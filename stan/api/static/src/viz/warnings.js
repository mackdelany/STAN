/*
 * warnings.js
 * 2020 STAN
 *
 * This function is used to parse and render triage warnings.
 *
 */


function renderWarnings(WarningList) {

    if (WarningList.length > 0) {

        let WarningsDiv = document.createElement("div");
        WarningsDiv.id = "warnings-template";

        var TitleElement = document.createElement("h2");
        var TitleText = document.createTextNode("Red flags");
        TitleElement.appendChild(TitleText);
        WarningsDiv.appendChild(TitleElement)

        for (var Warning in WarningList) {

            var WarningElement = document.createElement("p")
            var WarningText = document.createTextNode(WarningList[Warning])
            WarningElement.appendChild(WarningText)
            WarningsDiv.appendChild(WarningElement)

        }

        document.getElementById("stan-wrapper").appendChild(WarningsDiv);

    }

}