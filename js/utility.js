function httpGet(theUrl) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.responseText;
}

function checkFile(url) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", url, false); // false for synchronous request
    xmlHttp.send(null);
    return xmlHttp.status==200;
}

function camelCase(obj) {
    var newObj = {};
    for (d in obj) {
        if (obj.hasOwnProperty(d)) {
            newObj[d.replace(/(\_\w)/g, function(k) {
                return k[1].toUpperCase();
            })] = obj[d];
        }
    }
    return newObj;
}