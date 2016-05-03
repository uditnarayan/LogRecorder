$(function() {

	var heartbeat = new EventSource('/heartbeat');
	
	heartbeat.onmessage = function (beat) {
	  var data = JSON.parse(beat.data);
	  console.log(data);
	  updateGauges(data);
	};

	var gauges = [];			
	function createGauge(name, label, min, max)
	{
		var config = 
		{
			size: 200,
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
	
	function createGauges()
	{		
		createGauge("cpu", "CPU");
		createGauge("memory", "Memory");
	}
	
	function updateGauges(data)
	{
		gauges["cpu"].redraw(data.cpu);
		gauges["memory"].redraw(data.mem);		
	}
	
	function getRandomValue(gauge)
	{
		var overflow = 0; //10;
		return gauge.config.min - overflow + (gauge.config.max - gauge.config.min + overflow*2) *  Math.random();
	}
	
	function initialize()
	{
		createGauges();
		setInterval(updateGauges, 5000);
	}
	initialize();
});