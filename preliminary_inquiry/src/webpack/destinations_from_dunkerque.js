import data from '../static/data/destinations_from_dunkerque.json'
import * as d3 from 'd3'

const maxTonnage = [];
const onePerCent = maxTonnage / 100
console.log(onePerCent);

const scale = d3.scaleLinear()
  .domain([
    data.nodes.map(node => node.tonnage).sort()[0],
    data.nodes.map(node => node.tonnage).sort()[data.nodes.length - 1]
  ])
  .range([
    1,
    20
  ])

const graphProperties = {
  "attraction_force": 800,
  "attraction_distance_max": 600,
  "attraction_vertical": 0,
  "attraction_horizontal": 0
}

const view = {
  /**
   * Zoom and position on the graph
   * @type {object}
   * @default
   */
  position: {x: 0, y: 0, zoom: 1}
};

// console.log(
  
// );



data.nodes = data.nodes.map((node) => {
  node.size = scale(node.tonnage)
  node.label = node.id
  return node
})

window.svg = d3.select("#graph");

let svgSize = svg.node().getBoundingClientRect();

const width = svgSize.width;
const height = svgSize.height;

svg
  .attr("viewBox", [0, 0, width, height])
  .attr("preserveAspectRatio", "xMinYMin meet");

/** Force simulation
------------------------------------------------------------*/

const simulation = d3.forceSimulation(data.nodes)
  .force("link", d3.forceLink(data.links).id(d => d.id))
  .force("charge", d3.forceManyBody())
  .force("center", d3.forceCenter())
  .force("forceX", d3.forceX())
  .force("forceY", d3.forceY());

simulation.force("center")
  .x(width * 0.5)
  .y(height * 0.5);

window.updateForces = function () {
  // get each force by name and update the properties

  simulation.force("charge")
    // turn force value to negative number
    .strength(-Math.abs(graphProperties.attraction_force))
    .distanceMax(graphProperties.attraction_distance_max);

  simulation.force("forceX")
    .strength(graphProperties.attraction_horizontal)

  simulation.force("forceY")
    .strength(graphProperties.attraction_vertical)

  // restarts the simulation
  simulation.alpha(1).restart();
}

updateForces();

simulation
  .on("tick", function () {
    elts.links
      .attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    elts.nodes.attr("transform", function (d) {
      d.x = Math.max(d.size, Math.min(width - d.size, d.x));
      d.y = Math.max(d.size, Math.min(height - d.size, d.y));

      return "translate(" + d.x + "," + d.y + ")";
    });

    // d3.select('#load-bar-value')
    //   .style('flex-basis', (simulation.alpha() * 100) + '%');
  });

/** Elements
------------------------------------------------------------*/

const elts = {};

elts.links = svg.append("g")
  .selectAll("line")
  .data(data.links)
  .enter().append("line")
  .attr("class", (d) => 'l_' + d.type)
// .attr("title", (d) => d.title)
// .attr("data-source", (d) => d.source)
// .attr("data-target", (d) => d.target)
// .attr("stroke-dasharray", function (d) {
//   if (d.shape.stroke === 'dash' || d.shape.stroke === 'dotted') {
//     return d.shape.dashInterval
//   }
//   return false;
// })
// .attr("filter", function (d) {
//   if (d.shape.stroke === 'double') {
//     return 'url(#double)'
//   }
//   return false;
// });

// if (graphProperties.graph_arrows === true) {
//   elts.links
//     .attr("marker-end", 'url(#arrow)');
// }

elts.nodes = svg.append("g")
  .selectAll("g")
  .data(data.nodes)
  .enter().append("g")
  .attr("data-node", (d) => d.id)
// .on('click', function (d) {
//   openRecord(d.id);
// });

elts.circles = elts.nodes.append("circle")
  .attr("r", (d) => d.size)
  .attr("class", (d) => "n_" + d.type)
  .call(d3.drag()
    .on("start", function (d) {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    })
    .on("drag", function (d) {
      d.fx = d3.event.x;
      d.fy = d3.event.y;
    })
    .on("end", function (d) {
      if (!d3.event.active) simulation.alphaTarget(0.0001);
      d.fx = null;
      d.fy = null;
    })
  )
  .on('mouseenter', function (nodeMetas) {
    // if (!graphProperties.graph_highlight_on_hover) { return; }

    let nodesIdsHovered = [nodeMetas.id];

    const linksToModif = elts.links.filter(function (link) {
      if (link.source.id === nodeMetas.id || link.target.id === nodeMetas.id) {
        nodesIdsHovered.push(link.source.id, link.target.id);
        return false;
      }
      return true;
    })

    const nodesToModif = elts.nodes.filter(function (node) {
      if (nodesIdsHovered.includes(node.id)) {
        return false;
      }
      return true;
    })

    const linksHovered = elts.links.filter(function (link) {
      if (link.source.id !== nodeMetas.id && link.target.id !== nodeMetas.id) {
        return false;
      }
      return true;
    })

    const nodesHovered = elts.nodes.filter(function (node) {
      if (!nodesIdsHovered.includes(node.id)) {
        return false;
      }
      return true;
    })

    nodesHovered.classed('hover', true);
    linksHovered.classed('hover', true);
    nodesToModif.classed('translucent', true);
    linksToModif.classed('translucent', true);
  })
  .on('mouseout', function () {
    // if (!graphProperties.graph_highlight_on_hover) { return; }

    elts.nodes.classed('hover', false);
    elts.nodes.classed('translucent', false);
    elts.links.classed('hover', false);
    elts.links.classed('translucent', false);
  });

elts.labels = elts.nodes.append("text")
  .each(function (d) {
    const words = d.label.split(' ')
      , max = 25
      , text = d3.select(this);
    let label = '';

    for (let i = 0; i < words.length; i++) {
      // combine words and seperate them by a space caracter into label
      label += words[i] + ' ';

      // if label (words combination) is longer than max & not the single iteration
      if (label.length < max && i !== words.length - 1) { continue; }

      text.append("tspan")
        .attr('x', 0)
        .attr('dy', '1.2em')
        .text(label.slice(0, -1)); // remove last space caracter

      label = '';
    }
  })
  // .attr('font-size', graphProperties.graph_text_size)
  .attr('x', 0)
  .attr('y', (d) => d.size)
  .attr('dominant-baseline', 'middle')
  .attr('text-anchor', 'middle');


(function () {

  const zoomInterval = 0.3 // interval between two (de)zoom
    , zoomMax = 3
    , zoomMin = 1;

  svg.call(d3.zoom().on('zoom', function () {
    // for each move one the SVG

    if (d3.event.sourceEvent === null) {
      zoomMore();
      return;
    }

    switch (d3.event.sourceEvent.type) {
      case 'wheel':
        // by mouse wheel
        if (d3.event.sourceEvent.deltaY >= 0) {
          zoomLess();
        } else {
          zoomMore();
        }
        break;

      case 'mousemove':
        // by drag and move with mouse
        view.position.x += d3.event.sourceEvent.movementX;
        view.position.y += d3.event.sourceEvent.movementY;

        translate();
        break;
    }
  }));

  function zoomMore() {
    view.position.zoom += zoomInterval;

    if (view.position.zoom >= zoomMax) {
      view.position.zoom = zoomMax;
    }

    translate();
  }

  function zoomLess() {
    view.position.zoom -= zoomInterval;

    if (view.position.zoom <= zoomMin) {
      view.position.zoom = zoomMin;
    }

    translate();
  }

  function zoomReset() {
    view.position.zoom = 1;
    view.position.x = 0;
    view.position.y = 0;

    translate();
  }

  // export functions on global namespace
  window.zoomMore = zoomMore;
  window.zoomLess = zoomLess;
  window.zoomReset = zoomReset;

})();

/**
 * Change 'style' attribute of SVG to change view
 */

function translate() {
  svg.attr('style', `transform:translate(${view.position.x}px, ${view.position.y}px) scale(${view.position.zoom});`);
}

// var svg = d3.select("svg"),
//   width = +svg.attr("width"),
//   height = +svg.attr("height");

// var color = d3.scaleOrdinal(d3.schemeCategory20);

// var simulation = d3.forceSimulation()
//   .force("link", d3.forceLink().id(function (d) { return d.id; }))
//   .force("charge", d3.forceManyBody())
//   .force("center", d3.forceCenter(width / 2, height / 2));

// var link = svg.append("g")
//   .attr("class", "links")
//   .selectAll("line")
//   .data(graph.links)
//   .enter().append("line")
//   .attr("stroke-width", function (d) { return Math.sqrt(d.value); });

// var node = svg.append("g")
//   .attr("class", "nodes")
//   .selectAll("g")
//   .data(graph.nodes)
//   .enter().append("g")
//   .attr("r", (d) => d.size)

// var circles = node.append("circle")
//   .attr("r", 5)
//   .attr("fill", function (d) { return color(d.group); });

// // Create a drag handler and append it to the node object instead
// var drag_handler = d3.drag()
//   .on("start", dragstarted)
//   .on("drag", dragged)
//   .on("end", dragended);

// drag_handler(node);

// var lables = node.append("text")
//   .text(function (d) {
//     return d.id;
//   })
//   .attr('x', 6)
//   .attr('y', 3);

// node.append("title")
//   .text(function (d) { return d.id; });

// simulation
//   .nodes(graph.nodes)
//   .on("tick", ticked);

// simulation.force("link")
//   .links(graph.links);

// function ticked() {
//   link
//     .attr("x1", function (d) { return d.source.x; })
//     .attr("y1", function (d) { return d.source.y; })
//     .attr("x2", function (d) { return d.target.x; })
//     .attr("y2", function (d) { return d.target.y; });

//   node.attr("transform", function (d) {
//     console.log(d.size, width);
//     d.x = Math.max(d.size, Math.min(width - d.size, d.x));
//     d.y = Math.max(d.size, Math.min(height - d.size, d.y));

//     return "translate(" + d.x + "," + d.y + ")";
//   });

//   // node
//   //   .attr("transform", function (d) {
//   //     return "translate(" + d.x + "," + d.y + ")";
//   //   })
// }

// function dragstarted(d) {
//   if (!d3.event.active) simulation.alphaTarget(0.3).restart();
//   d.fx = d.x;
//   d.fy = d.y;
// }

// function dragged(d) {
//   d.fx = d3.event.x;
//   d.fy = d3.event.y;
// }

// function dragended(d) {
//   if (!d3.event.active) simulation.alphaTarget(0);
//   d.fx = null;
//   d.fy = null;
// }

// =====================
// =====================
// =====================
// =====================



// import * as vis from "vis-network/dist/vis-network";

// data.nodes = data.nodes.map((node) => {
//   return {
//     id: node.id,
//     label: node.pays
//   }
// })

// data.links = data.links.map((link) => {
//   return {
//     from: link.source,
//     to: link.target
//   }
// })

// // console.log(
// //   data.nodes,
// //   data.links
// // );

// var nodes = new vis.DataSet(data.nodes);

//   // create an array with edges
//   var edges = new vis.DataSet(data.links);

//   // create a network
//   var container = document.getElementById("container");
//   var toto = {
//     nodes: nodes,
//     edges: edges,
//   };
//   var options = {
//     layout: {
//       improvedLayout: false
//     }
//   };
//   var network = new vis.Network(container, toto, options);