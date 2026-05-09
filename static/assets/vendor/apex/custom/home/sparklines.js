// Sparkline 1
var options1 = {
	series: [
		{
			name: "Chrome",
			data: [5, 9, 7, 14, 25, 20, 27, 22, 18, 24, 19],
		},
	],
	chart: {
		type: "line",
		width: 90,
		height: 20,
		sparkline: {
			enabled: true,
		},
	},
	xaxis: {
		crosshairs: {
			width: 1,
			categories: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
		},
	},
	stroke: {
		show: true,
		lineCap: "butt",
		colors: ["#e50000"],
		width: 3,
		dashArray: 0,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return val + " %";
			},
		},
	},
};
var chart1 = new ApexCharts(document.querySelector("#sparkline1"), options1);
chart1.render();

// Sparkline 2
var options2 = {
	series: [
		{
			name: "Firefox",
			data: [5, 9, 7, 14, 25, 20, 27, 22, 18, 24, 19],
		},
	],
	chart: {
		type: "line",
		width: 90,
		height: 20,
		sparkline: {
			enabled: true,
		},
	},
	xaxis: {
		crosshairs: {
			width: 1,
			categories: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
		},
	},
	stroke: {
		show: true,
		lineCap: "butt",
		colors: ["#008d02"],
		width: 3,
		dashArray: 0,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return val + " %";
			},
		},
	},
};
var chart2 = new ApexCharts(document.querySelector("#sparkline2"), options2);
chart2.render();

// Sparkline 3
var options3 = {
	series: [
		{
			name: "Microsoft Edge",
			data: [5, 9, 7, 14, 25, 20, 27, 22, 18, 24, 19],
		},
	],
	chart: {
		type: "line",
		width: 90,
		height: 20,
		sparkline: {
			enabled: true,
		},
	},
	xaxis: {
		crosshairs: {
			width: 1,
			categories: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
		},
	},
	stroke: {
		show: true,
		lineCap: "butt",
		colors: ["#006be5"],
		width: 3,
		dashArray: 0,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return val + " %";
			},
		},
	},
};
var chart3 = new ApexCharts(document.querySelector("#sparkline3"), options3);
chart3.render();

// Sparkline 4
var options4 = {
	series: [
		{
			name: "Opera",
			data: [5, 9, 7, 14, 25, 20, 27, 22, 18, 24, 19],
		},
	],
	chart: {
		type: "line",
		width: 90,
		height: 20,
		sparkline: {
			enabled: true,
		},
	},
	xaxis: {
		crosshairs: {
			width: 1,
			categories: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"],
		},
	},
	stroke: {
		show: true,
		lineCap: "butt",
		colors: ["#7d0c9d"],
		width: 3,
		dashArray: 0,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return val + " %";
			},
		},
	},
};
var chart4 = new ApexCharts(document.querySelector("#sparkline4"), options4);
chart4.render();
