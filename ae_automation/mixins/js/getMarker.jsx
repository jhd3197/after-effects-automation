//
// Rename Item
// ------------------------------------------------------------
// Language: javascript
//


var layer = app.project.activeItem.selectedLayers[0];
var myComp = app.project.activeItem;
var myLayer = myComp.layer(1);
if (myComp.markerProperty.numKeys > 0){
alert(myComp.markerProperty.keyTime(1));

var myLayer = myComp.layer(2).property("Cut");
alert(myLayer);
}