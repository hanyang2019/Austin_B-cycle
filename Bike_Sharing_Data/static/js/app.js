
d3.json("/All").then(function(data) {
  var data = [data];
  
  
  Plotly.plot("bar", data);

});
// margin: { t: 30, b: 100, pad: 4 }
function updatePlotly(newdata) {
  Plotly.restyle("bar", "x", [newdata.x]),
  Plotly.restyle("bar", "y", [newdata.y]),
  Plotly.restyle("bar", "fill", [newdata.fill]),
  Plotly.restyle("bar", "type", [newdata.type]);
  console.log([newdata.x])
};

function getData(route) {
  console.log(route);
  d3.json(`/${route}`).then(function(data) {
    console.log("newdata", data);
    updatePlotly(data);
  });
}

function init() {
    // Grab a reference to the dropdown select element
    var selector = d3.select("#selDataset");
    console.log(selector)
    // Use the list of sample names to populate the select options
    d3.json("/options").then((Options) => {
      console.log(Options)
      Options.forEach((pick) => {
        selector
          .append("option")
          .text(pick)
          .property("value", pick);
      });
    // const firstOption = "Day";
    // buildCharts(firstOption);
    
      });
};

init();

