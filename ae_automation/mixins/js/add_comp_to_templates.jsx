//
// Add component to templates
// ------------------------------------------------------------
// Language: javascript
//

_comp=FindItemByName("{compName}");

_comp.layers.add(app.project.items[{CompTemplateID}]);

_comp.layers[1].startTime ={start_time};
_comp.layers[1].inPoint  = {inPoint};
_comp.layers[1].stretch  = {stretch};
_comp.layers[1].outPoint  = {end_time};