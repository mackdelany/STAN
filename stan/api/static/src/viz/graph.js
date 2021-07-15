function prepareGraph(graphDiv, graph_height){
    margin = {top: 0, right: 20, bottom: 35, left: 20},
    width = 800 - margin.left - margin.right,
    height = graph_height - margin.top - margin.bottom;


  svg = d3.select(graphDiv)
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");


  x = d3.scaleLinear()
    .domain([0.7, 5.3])    
    .range([0, width]);
    svg.append("g")
    .style("font-size", "30px")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(x).ticks(5));


  y = d3.scaleLinear()
    .range([height, 0]);
    y.domain([0, 900]);   
    //svg.append("g")
    //.call(d3.axisLeft(y));
};

function buildGraph(data, triageCode){

  var histogram = d3.histogram()
      .domain(x.domain())  
      .thresholds(x.ticks(20));

  var bins = histogram(data)

  var graph = svg.selectAll("rect")
        .data(bins)

      graph.enter()
        .append("rect")
        .merge(graph)
        .transition()
        .duration(2000)
          .attr("x", 1)
          .attr("transform", function(d) { return "translate(" + x(d.x0) + "," + y(d.length) + ")"; })
          .attr("width", function(d) { return x(d.x1) - x(d.x0) -1 ; })
          .attr("height", function(d) { return height - y(d.length); })
          .style("fill", function() {if (triageCode > 4.25) {return "#a65628";} 
                                    else if (triageCode > 3.5){return "#377eb8";} 
                                    else if (triageCode > 2.5){return "#69b3a2";} 
                                    else if (triageCode > 1.75){return "#ff7f00";} 
                                    else {return "#e41a1c"} });
      
      graph.exit()
        .remove();
}

prepareGraph("#triage-graph", 400);