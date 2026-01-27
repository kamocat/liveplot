const opts = {
	title: "Acceleration",
	id: "chart1",
	class: "mychart",
	width: window.innerWidth*0.7,
	height: window.innerHeight*0.8,
	series: [
		{
			scale: "seconds",
			label: "seconds",
		},{
			scale: "acceleration",
			label: "X",
			stroke:"red",
			width: 1,
		},{
			scale: "acceleration",
			label: "Y",
			stroke:"green",
			width: 1,
		},{
			scale: "acceleration",
			label: "Z",
			stroke:"blue",
			width: 1,
		},
	],
	scales: {
		"seconds": {
			time: false,
		},
		"acceleration": {
			auto: true,
		},
	},
}

var stats;

function printStats(data){
	let axes = ['X','Y','Z'];
	let s = '';
	stats = data.slice(1,4).map(a => [Math.min(...a),Math.max(...a)]);
	for(let i=0; i<3; ++i){
		s += axes[i]+'_Min:'+stats[i][0]+"<br>";
		s += axes[i]+'_Max:'+stats[i][1]+"<br>";
	}
	let e = document.getElementById("stats");
	e.innerHTML = s;
}

let axes = ["X accel","Y accel","Z accel"]
function set_axes_options(){
	let e = document.getElementById("axis")
	for( a of axes ){
		let n = document.createElement("option")
		n.innerHTML = a
		e.appendChild(n)
	}
}
function get_axes(){
	let e = document.getElementById("axis")
	return axes.findIndex((v) => e.value == v)
}
set_axes_options();

function autorange(){
	let axis = get_axes()
	let minv = stats[axis][0]
	let maxv = stats[axis][1]
	margin = 0.1 * (maxv - minv)
	document.getElementById("minv").value = minv - margin
	document.getElementById("maxv").value = Number(maxv) + margin
}

let trig_timer = 0
function get_trigger(){
	let trg = document.getElementById("trg")
	let enabled = document.getElementById("en").checked
	let axis = get_axes()
	let minv = document.getElementById("minv").value
	let maxv = document.getElementById("maxv").value
	let timeout = document.getElementById("timeout").value * 1000
	if( !enabled ){
		trg.checked = false
	} else if((minv < stats[axis][0]) && maxv > stats[axis][1]){
		if((Date.now() - trig_timer) >  timeout){
			trg.checked = false
		}
	} else {
		trg.checked = true
		trig_timer = Date.now()
	}
	return trg.checked
}


async function loop(){

	const socket = new WebSocket("/stream")
let data = [[], [], [], []]
	let plot = new uPlot(opts, data, document.getElementById("chart1"))
	let wt = false
	socket.addEventListener("message", (event) => {
		let nd = JSON.parse(event.data)
		for (i = 0; i < 4; i++){
			data[i] = data[i].concat(nd[i])
		}
		printStats(data)
		plot.setData(data)
	})
	await new Promise(r => requestAnimationFrame(r));//For production
}
loop();

function tail(data){
	let t = [];
	t = [t].concat(data);
	return t;
}

function pretty(matrix) {
	// Seperates the lines with newline instead of brackets
	return matrix.map(row => row+'\r\n');
}

function save_recording(data) {
	file = new Blob(pretty(data), {type:"octet/stream"});
	tag = document.createElement("li");
	tag.innerHTML = '<a href="'+URL.createObjectURL(file)+'" download="acceleration_log.csv">Download</a>';
	document.getElementById("dl").appendChild(tag);
}

