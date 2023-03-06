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
			auto: false,
			range: [-16, 16]
		},
	},
}
async function getData(t0){
	return fetch("/data/"+t0)
		.then((response) => response.json())
		.then((data) => {
			t = [];
			n = data.x.length;
			for(let i = 0; i<n; ++i){
				t.push(i+data.t0);
			}
			return [t,data.x,data.y,data.z];
	});
}

function printStats(data){
	axes = ['X','Y','Z'];
	let s = '';
	for(let i=0; i<3; ++i){
		s += axes[i]+' Min:'+Math.min(...data[i+1])+"<br>";
		s += axes[i]+' Max:'+Math.max(...data[i+1])+"<br>";
	}
	let e = document.getElementById("stats");
	e.innerHTML = s;
}

async function loop(){
	let data = await getData(0);
	let plot = new uPlot(opts, data, document.getElementById("chart1"));
	for(;;){
		let t0 = Number(data[0].slice(-1))+1;
		console.log(t0);
		let newdata = await getData(t0);
		for(let i = 0; i < data.length; ++i){
			let a = data[i].concat(newdata[i]);
			data[i] = a.slice(-6000,-1);
		}
		printStats(data);
		plot.setData(data);
		//save_recording(data);
		await new Promise(r => setTimeout(r, 2000)); //For testing
		await new Promise(r => requestAnimationFrame(r));//For production
	}
}
loop();

function transpose(matrix) {
	return matrix[0].map((col, i) => matrix.map(row => row[i]));
}

function pretty(matrix) {
	// Seperates the lines with newline instead of brackets
	return matrix.map(row => row+'\r\n');
}

function save_recording(data) {
	enabled = document.getElementById("en").checked;
	file = new Blob(pretty(transpose(data)), {type:"octet/stream"});
	tag = document.createElement("li");
	tag.innerHTML = '<a href="'+URL.createObjectURL(file)+'" download="acceleration_log.csv">Download</a>';
	document.getElementById("dl").appendChild(tag);
}
