var width = 960,
    height = 500;

var color = d3.scale.category20();

var force = d3.layout.force()
    .charge(-1500)
    .linkDistance(200)
    .size([width, height]);

var svg = d3.select("#chart").append("svg")
    .attr("width", width)
    .attr("height", height);

g_data = { nodes : d3.map(), links : d3.map() }

function update_nodes( parentnode ){
	return function(json) {
		for( i in json.nodes ){
			n = json.nodes[i]
			if( parentnode ){
				n.x = parentnode.x - 5 + 10 * Math.random();
				n.y = parentnode.y - 5 + 10 * Math.random();
			}
			g_data.nodes.set( n.name, n);
		}
		nodes_str = '["' + g_data.nodes.keys().join('","') + '"]'
		d3.json("http://0.0.0.0:4567/flows/?accounts="+escape(nodes_str), function(json){
			repaint({nodes: g_data.nodes.values(), links: json.links});
		});
	}
}

function repaint(data) {
	console.log(data.links)
	var link = svg.selectAll("line.link")
		.data(data.links)

	link.enter().append("line")
		.attr("class", "link")
		.style("stroke-width", function(d) { return Math.sqrt(d.value); });

	link.attr("class", "link")
		.style("stroke-width", function(d) { return Math.sqrt(d.value); });

	link.exit().remove();

    var node = svg.selectAll("g.node")
		.data(data.nodes, function(d){ return d.name } )

	node.select("circle")
      .attr("r", function(d){ return Math.sqrt(d.value); })
      .style("fill", function(d) { return color(d.group); })

	node.select("text")
      .attr("class", "value")
      .attr("text-anchor", "middle")
      .text(function(d) { return d.name+"\n"+d.value; });

	node.exit().remove();

	var groups = node.enter().append("g")
        .attr("class", "node")
        .call(force.drag)		

	groups.append("circle")
      .attr("r", function(d){ return Math.sqrt(d.value); })
      .style("fill", function(d) { return color(d.group); })

	groups.append("text")
      .attr("class", "value")
      .attr("text-anchor", "middle")
      .text(function(d) { return d.name+"\n"+d.value; });

  node.on("click", function(d) {
	g_data.nodes.remove(d.name);
	console.log(d)
	g_data.links.forEach( function(k,v){
		console.log(k);
		if( v.source == d || v.target == d ){
			console.log(v);
			g_data.links.remove(k);
		}
	});
	d3.json("http://0.0.0.0:4567/balances/"+d.name, update_nodes(d));
  });

  force
      .nodes(svg.selectAll("g.node").data())
      .links(svg.selectAll("line.link").data())
      .start();

  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

	node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
}

d3.json("http://0.0.0.0:4567/balances/", update_nodes(null) );
