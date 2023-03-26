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
	axes = ['X','Y','Z'];
	let s = '';
	stats = data.slice(1,4).map(a => [Math.min(...a),Math.max(...a)]);
	for(let i=0; i<3; ++i){
		s += axes[i]+'_Min:'+stats[i][0]+"<br>";
		s += axes[i]+'_Max:'+stats[i][1]+"<br>";
	}
	let e = document.getElementById("stats");
	e.innerHTML = s;
}

function autorange(){
	let x_min = stats[0][0];
	let x_max = stats[0][1];
	margin = 0.1 * (x_max - x_min);
	document.getElementById("minv").value = x_min - margin;
	document.getElementById("maxv").value = Number(x_max) + margin;
}

/**
 * This transformer takes binary Uint8Array chunks from a `fetch`
 * and translates them to chunks of strings.
 *
 * @implements {TransformStreamTransformer}
 */
class Uint8ArrayToJsonTransformer {
  constructor() {
    this.decoder = new TextDecoder()
    this.lastString = ''
  }

  /**
   * Receives the next Uint8Array chunk from `fetch` and transforms it.
   *
   * @param {Uint8Array} chunk The next binary data chunk.
   * @param {TransformStreamDefaultController} controller The controller to enqueue the transformed chunks to.
   */
  transform(chunk, controller) {
    //console.log('Received chunk %o with %d bytes.', chunk, chunk.byteLength)

    // Decode the current chunk to string and prepend the last string
    const string = `${this.lastString}${this.decoder.decode(chunk)}`

    // Extract lines from chunk
    const lines = string.split(/\r\n|[\r\n]/g)

    // Save last line, as it might be incomplete
    this.lastString = lines.pop() || ''

    // Enqueue each line in the next chunk
    for (const line of lines) {
      controller.enqueue(JSON.parse(line).data)
    }
  }

  /**
   * Is called when `fetch` has finished writing to this transform stream.
   *
   * @param {TransformStreamDefaultController} controller The controller to enqueue the transformed chunks to.
   */
  flush(controller) {
    // Is there still a line left? Enqueue it
    if (this.lastString) {
      controller.enqueue(this.lastString)
    }
  }
}


async function loop(){

    // Create a transform stream with our transformer
    const ts = new TransformStream(new Uint8ArrayToJsonTransformer())
    // Fetch the text file
    const response = await fetch('/stream')
    // Get a ReadableStream on the text file's body
    const rs = response.body
    // Apply our Transformer on the ReadableStream to create a stream of strings
    const lineStream = rs.pipeThrough(ts)
    // Read the stream of strings
    const stream = lineStream.getReader()
  
    let data = await stream.read().then((d) => d.value)
    console.log(data)
	let plot = new uPlot(opts, tail(data), document.getElementById("chart1"))
	for(;;){
        await stream.read().then((d) => d.value)
            .then((newdata) => {
            data = data.concat(newdata)
            //printStats(data)
            plot.setData(tail(data))
            //logData(newdata)
        })
		await new Promise(r => requestAnimationFrame(r));//For production
	}
}
loop();

function tail(data){
    vals = data.slice(-6000,-1);
    let t = [];
    for (let i = data.length - vals.length; i < data.length; ++i){
        t.push(i*0.01);
    }
    t = [t].concat(transpose(vals));
    return t;
}

function transpose(matrix) {
	return matrix[0].map((col, i) => matrix.map(row => row[i]));
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

var logged=[[],[],[],[]];
let timeout=0;
function logData(newdata){
	enabled = document.getElementById("en").checked;
	notEmpty = logged[0].length > 0;
	//For now, only works with X axis
	if(enabled){
		if((Math.min(...newdata[1])<document.getElementById("minv").value)
		 || (Math.max(...newdata[1])>document.getElementById("maxv").value)){
			 timeout=0;
		 } else {
			 ++timeout;
		 }
		if(notEmpty && (timeout > document.getElementById("timeout").value)){
			save_recording(logged);
			logged=[[],[],[],[]];
		} else {
			for(let i = 0; i < newdata.length; ++i){
				let a = logged[i].concat(newdata[i]);
				logged[i] = a.slice(-6000,-1);
			}
		}
	} else if(notEmpty){
		save_recording(logged);
		logged=[[],[],[],[]];
	}
}

