var LOG_OUTPUT = false;
var _LOGS = ""
var CACHE_FODLER = "{CACHE_FOLDER}";

function FindItemIdByName(name) {
    var projectItems = app.project.items;
    for (var i = 1; i <= projectItems.length; i++) {
        if (projectItems[i].name == name) {
            return i;
        }
    }
    return null;
}

function FindItemByName(name) {
    return app.project.item(FindItemIdByName(name));
}

function FindLayerByComp(compName,layer_name) {
    var projectItems = app.project.items;
    for (var ee = 1; ee <= projectItems.length; ee++) {
        if (projectItems[ee].name == compName) {
            comp = app.project.item(ee);
            for(var i = 1; i <= comp.layers.length; i++) {
                if(comp.layers[i].name==layer_name){
                    return comp.layers[i];
                }
            }
        }
    }
    return null;
}

function FindLayerByLayerIndex(compName,layer_index) {
    var projectItems = app.project.items;
    for (var ee = 1; ee <= projectItems.length; ee++) {
        if (projectItems[ee].name == compName) {
            comp = app.project.item(ee);
            for(var i = 1; i <= comp.layers.length; i++) {
                if(layer_index ==i){
                    return comp.layers[i];
                }
            }
        }
    }
    return null;
}

function slugify(str) {
    str = str.replace(/^\s+|\s+$/g, ''); // trim
    str = str.toLowerCase();
  
    // remove accents, swap ñ for n, etc
    var from = "àáäâèéëêìíïîòóöôùúüûñç·/_,:;";
    var to   = "aaaaeeeeiiiioooouuuunc------";
    for (var i=0, l=from.length ; i<l ; i++) {
        str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
    }

    str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
        .replace(/\s+/g, '-') // collapse whitespace and replace by -
        .replace(/-+/g, '-'); // collapse dashes

    return str;
}

function saveFile(fileName,fileContent){
    var _file = File(CACHE_FODLER+fileName);
    _file.open("w");
    _file.writeln(fileContent);
    _file.close();
}

function print(log,log2,log3){
    // Add time of the log
    var date = new Date();
    var time = date.toJSON();
    var separator = " , ";
    if(log2 == undefined){
        log2 = "";
        separator = "";
    }
    var separator3 = " , ";
    if(log3 == undefined){
        log3 = "";
        separator3 = "";
    }

    try{
        _LOGS += time + " : " + log.toString() + separator + log2.toString() + separator3 + log3.toString() + "\n";
    }
    catch(e){
        try{
            _LOGS += time + " : " + log + separator + log2  + separator3 + log3+ "\n";
        }
        catch(e){
            _LOGS += time + " : Error \n";
        }
    }
}

function outputLogs(finalLog,debug){
    //if finalLog is undefined
    if(finalLog == undefined){
        finalLog = "";
    }
    _LOGS = _LOGS + "\n" + finalLog;

    /*
    Code for Import https://scriptui.joonas.me — (Triple click to select): 
    {"activeId":6,"items":{"item-0":{"id":0,"type":"Dialog","parentId":false,"style":{"enabled":true,"varName":null,"windowType":"Dialog","creationProps":{"su1PanelCoordinates":false,"maximizeButton":false,"minimizeButton":false,"independent":false,"closeButton":true,"borderless":false,"resizeable":false},"text":"Dialog","preferredSize":[0,0],"margins":16,"orientation":"column","spacing":10,"alignChildren":["center","top"]}},"item-2":{"id":2,"type":"Panel","parentId":0,"style":{"enabled":true,"varName":null,"creationProps":{"borderStyle":"etched","su1PanelCoordinates":false},"text":"Log","preferredSize":[0,0],"margins":10,"orientation":"column","spacing":10,"alignChildren":["left","top"],"alignment":null}},"item-4":{"id":4,"type":"EditText","parentId":2,"style":{"enabled":true,"varName":null,"creationProps":{"noecho":false,"readonly":true,"multiline":true,"scrollable":true,"borderless":false,"enterKeySignalsOnChange":false},"softWrap":false,"text":"EditText\nsdsds","justify":"left","preferredSize":[700,200],"alignment":"right","helpTip":null}},"item-5":{"id":5,"type":"Button","parentId":0,"style":{"enabled":true,"varName":null,"text":"Close","justify":"center","preferredSize":[0,0],"alignment":"right","helpTip":null}},"item-6":{"id":6,"type":"StaticText","parentId":0,"style":{"enabled":true,"varName":null,"creationProps":{"truncate":"none","multiline":false,"scrolling":false},"softWrap":false,"text":"File : {FILE_NAME}","justify":"left","preferredSize":[0,0],"alignment":"left","helpTip":null}}},"order":[0,6,2,4,5],"settings":{"importJSON":true,"indentSize":false,"cepExport":false,"includeCSSJS":true,"showDialog":true,"functionWrapper":false,"afterEffectsDockable":false,"itemReferenceList":"None"}}
    */ 

    // DIALOG
    // ======
    var dialog = new Window("dialog"); 
    dialog.text = "AE Automation - Debug"; 
    dialog.orientation = "column"; 
    dialog.alignChildren = ["center","top"]; 
    dialog.spacing = 10; 
    dialog.margins = 16; 

    var statictext1 = dialog.add("statictext", undefined, undefined, {name: "statictext1"}); 
        statictext1.text = "File : {FILE_NAME}"; 
        statictext1.alignment = ["left","top"]; 

    // PANEL1
    // ======
    var panel1 = dialog.add("panel", undefined, undefined, {name: "panel1"}); 
        panel1.text = "Log"; 
        panel1.orientation = "column"; 
        panel1.alignChildren = ["left","top"]; 
        panel1.spacing = 10; 
        panel1.margins = 10; 

    var edittext1 = panel1.add('edittext {size: [700,400], properties: {name: "edittext1", readonly: true, multiline: true, scrollable: true}}'); 
        edittext1.text =_LOGS; 

    // DIALOG
    // ======
    var button1 = dialog.add("button", undefined, undefined, {name: "button1"}); 
        button1.text = "Close"; 
        button1.preferredSize.width = 700; 
        button1.alignment = ["center","top"]; 
        
        button1.onClick = function() { //user cancelled action
            dialog.close();
            return false;
        };
        
    debug=true;    
    //convert debug str to boolean
    if(debug == undefined){
        debug = false;
    }

    var STR_LOGS=_LOGS.toString();
    // Remove white spaces
    STR_LOGS = STR_LOGS.replace(/\s+/g, '');
    // Remove new lines
    STR_LOGS = STR_LOGS.replace(/\n+/g, '');
    // Remove tabs
    STR_LOGS = STR_LOGS.replace(/\t+/g, '');
    if(STR_LOGS==""){
        debug=false;
    }
    if(debug){
        //dialog.show();
    }
    //dialog.show();
}

function decodeHTMLEntities(text) {
    var entities = [
        ['amp', '&'],
        ['apos', '\''],
        ['#x27', '\''],
        ['#x2F', '/'],
        ['#39', '\''],
        ['#47', '/'],
        ['lt', '<'],
        ['gt', '>'],
        ['#44', ','],
        ['nbsp', ' '],
        ['quot', '"'],
        
    ];

    for (var i = 0, max = entities.length; i < max; ++i) 
        text = text.replace(new RegExp('&'+entities[i][0]+';', 'g'), entities[i][1]);

    return text;
}
    
function propertyParser(property, propertyName) {
    // Split property name by "."
    var propertyArray = propertyName.split(".");
    // Loop through property array
    for (var i = 0; i < propertyArray.length; i++) {
        // Get property
        property = property[propertyArray[i]];
    }
    return property
}

function valueParser(propertyValue){
    // If propertyValue contains [,] then it is an array
    if (propertyValue.indexOf(",") > -1 && propertyValue.indexOf("[") > -1 && propertyValue.indexOf("]") > -1) {
        //Remove first and last bracket
        propertyValue = propertyValue.substring(1, propertyValue.length - 1);
        // Split propertyValue by ","
        propertyValue = propertyValue.split(",");
    }
    else{
        // Decode html entities
        propertyValue = decodeHTMLEntities(propertyValue);
    }
    // check if value contains "<br>" and convert to "\n"s
    if (propertyValue.indexOf("<br>") > -1) {
        propertyValue = propertyValue.replace(/<br>/g, "\n");
    }
    return propertyValue
}

function deselectAll(){
    // deselect all comp
    var projectItems = app.project.items;
    for (var i = 1; i <= projectItems.length; i++) {
        app.project.item(i).selected = false;
    }
}

function deselectAllLayers(){
    var mySelection = app.project.activeItem;
    for(var i = 1; i <= mySelection.layers.length; i++) {
        comp.layers[i].selected = false;
    }
}