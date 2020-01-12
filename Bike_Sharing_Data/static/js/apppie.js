

function buildCharts(year) {

    var chartsURL = "/samples/" + year;
    d3.json(chartsURL).then(function(data) {
        console.log(chartsURL);
        console.log(data);
    
        var data = [{
            values: data.Counts,
            labels: data.Membership,
            hovertext: data.labels,
            type: 'pie',
        }];

        var layout = {
            showlegend: true,
        };

        Plotly.newPlot('pie', data, layout);

        
    }
    
    )
}



function init() {
//Grab a reference to the dropdown select element
var selector = d3.select("#selDataset2");

d3.json("/names").then((yearNames) => {
    console.log(yearNames);
    yearNames.forEach((year) => {
        console.log(year);
        selector
            .append("option")
            .text(year)
            .property("value", year);
    });

const firstSample = yearNames[0];
buildCharts(firstSample);

});

}

function optionChanged(newYear) {
buildCharts(newYear);
}

//Initialize the dashboard
init();

