// Pie #1
var options = {
	chart: {
		width: 320,
		type: "pie",
	},
	labels: ["USA", "IND", "GER", "BRZ", "TRK"],
	series: [20, 20, 20, 20, 20],
	legend: {
		position: "bottom",
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		width: 0,
	},
	colors: ["#ef0000", "#999999", "#aaaaaa", "#cccccc", "#eeeeee"],
};
var chart = new ApexCharts(document.querySelector("#pie1"), options);
chart.render();

// Pie #2
var options = {
	chart: {
		width: 320,
		type: "pie",
	},
	labels: ["USA", "IND", "GER", "BRZ", "TRK"],
	series: [20, 20, 20, 20, 20],
	legend: {
		position: "bottom",
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		width: 0,
	},
	colors: ["#ef0000", "#999999", "#aaaaaa", "#cccccc", "#eeeeee"],
};
var chart = new ApexCharts(document.querySelector("#pie2"), options);
chart.render();

// Pie #3
var options = {
	chart: {
		width: 320,
		type: "pie",
	},
	labels: ["USA", "IND", "GER", "BRZ", "TRK"],
	series: [20, 20, 20, 20, 20],
	legend: {
		position: "bottom",
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		width: 0,
	},
	colors: ["#ef0000", "#999999", "#aaaaaa", "#cccccc", "#eeeeee"],
};
var chart = new ApexCharts(document.querySelector("#pie3"), options);
chart.render();
