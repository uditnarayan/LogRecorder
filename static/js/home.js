$(function() {

	var gauges = [];			
	function createGauge(name, label, min, max)
	{
		var config = 
		{
			size: 220,
			label: label,
			min: undefined != min ? min : 0,
			max: undefined != max ? max : 100,
			minorTicks: 5
		}
		
		var range = config.max - config.min;
		config.yellowZones = [{ from: config.min + range*0.75, to: config.min + range*0.9 }];
		config.redZones = [{ from: config.min + range*0.9, to: config.max }];
		
		gauges[name] = new Gauge(name + "GaugeContainer", config);
		gauges[name].render();
	}
	
	function updateGauges(data)
	{
		gauges["cpu"].redraw(data.cpu);
		gauges["memory"].redraw(data.mem);		
		$('#rpsValue').text(data.rps);
	}
	
	function getRandomValue(gauge)
	{
		var overflow = 0; //10;
		return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow*2) *  Math.random();
	}
	
	function initilialze()
	{		
		createGauge("cpu", "CPU");
		createGauge("memory", "Memory");

		var xhr = $.ajax({
	        type: "GET",
	        data: {},
	        url: "/messages",
	        dataType: "json",
	        success: function (arg) {
	        	resp = JSON.parse(arg);
	        	if(resp.length == 0){
	        		var tr = $('<tr>',{class:"file-item"});
	            	tr.append($('<td>',{class:"file-name", text:"No message files."}));
	            	tr.append($('<td>',{class:"file-date", text:" "}));
	            	$('#logFileList').append(tr);
	        	}
	        	else{
		            $.each(resp, function(i,v){	        
		            	if(i % 2 == 0)
		            		classname = "file-item li-even"
		            	else
		            		classname = "file-item li-even"

		            	var tr = $('<tr>',{class:classname});
		            	tr.append($('<td>',{class:"file-name", text:v.file}));
		            	tr.append($('<td>',{class:"file-date", text:v.date}));
		            	$('#logFileList').append(tr);
		            });
	        	}
	        },
	        timeout: 30000,
	        error: function (request, error) {
	            console.log(error);
	            var tr = $('<tr>',{class:"file-item"});
	            tr.append($('<td>',{class:"file-name", text:"Cannot get list of message files."}));
	            tr.append($('<td>',{class:"file-date", text:" "}));
	            $('#logFileList').append(tr);
	        },
	        async: false
	    });

	    var heartbeat = new EventSource('/heartbeat');
	
		heartbeat.onmessage = function (beat) {
		  var data = JSON.parse(beat.data);
		  //console.log(data);
		  updateGauges(data);
		};
	}

	initilialze();
});