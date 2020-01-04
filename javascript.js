function initialize_webiopi() {
    // webiopiの準備が終わってからstyles.cssを適用する
    applyCustomCss("styles.css");

    // GPIOの状態を監視しない
    webiopi().refreshGPIO(false);
}

function clickEvent() {
    var execDate = document.myform.execTime.value;
    if (execDate == "") {
        webiopi().callMacro("clearCron", []);
    } else {
        webiopi().callMacro("updateCron", [execDate]);
    }
}

function applyCustomCss(custom_css) {
    var head = document.getElementsByTagName("head")[0];
    var style = document.createElement("link");
    style.rel = "stylesheet";
    style.type = "text/css";
    style.href = custom_css;
    head.appendChild(style);
}

function setDefault() {
    var getDefault = function(macro, args, response) {
        if (response) {
            document.getElementById("execTime").value = response;
        } else {
            document.getElementById("execTime").value = "";
        }
    };
    webiopi().callMacro("getCurrentSetting", [], getDefault);
}

window.onload = function() {
    setDefault();
};
