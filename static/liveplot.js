const opts = {
	title: "Acceleration",
	id: "chart1",
	class: "mychart",
	width: window.innerWidth,
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

async function loop(){
	let data = await getData(0);
	let plot = new uPlot(opts, data, document.getElementById("chart1"));
	for(;;){
		// Our loop is most likely limited by network delay
		// So no need to use requestAnimationFrame()
		let t0 = Number(data[0].slice(-1))+1;
		console.log(t0);
		let newdata = await getData(t0);
		for(let i = 0; i < data.length; ++i){
			let a = data[i].concat(newdata[i]);
			data[i] = a.slice(-1000,-1);
		}
		plot.setData(data);
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

	

var recording = false;
function toggle_recording() {
	button = document.getElementById("ctrl");
	if(recording){ //Recording is completed. Start the download. 
		file = new Blob(pretty(transpose(og)), {type:"octet/stream"});
  document.getElementById("dl").href=URL.createObjectURL(file);
		button.innerText = "Start Recording";
		recording = false;
	} else { // Begin the recording
		og = false;
		button.innerText = "Recording...";
		recording = true;
	}
}
