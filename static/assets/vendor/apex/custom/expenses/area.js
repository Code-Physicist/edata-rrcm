var options = {
	chart: {
		height: 300,
		type: "area",
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		curve: "smooth",
		width: 3,
		colors: ["#000000", "#999999", "#D6DAE3"],
	},
	series: [
		{
			name: "Expenses",
			data: [10, 20, 15, 30, 20, 35, 20, 40, 31, 43, 56, 29],
		},
	],
	grid: {
		borderColor: "#ccd2da",
		strokeDashArray: 5,
		xaxis: {
			lines: {
				show: true,
			},
		},
		yaxis: {
			lines: {
				show: false,
			},
		},
		padding: {
			top: 0,
			right: 0,
			bottom: 10,
			left: 0,
		},
	},
	xaxis: {
		categories: [
			"Jan",
			"Feb",
			"Mar",
			"Apr",
			"May",
			"Jun",
			"Jul",
			"Aug",
			"Sep",
			"Oct",
			"Nov",
			"Dec",
		],
	},
	yaxis: {
		labels: {
			show: false,
		},
	},
	colors: ["#000000", "#999999", "#D6DAE3"],
	markers: {
		size: 0,
		opacity: 0.7,
		colors: ["#000000", "#999999", "#D6DAE3"],
		strokeColor: "#ffffff",
		strokeWidth: 2,
		hover: {
			size: 7,
		},
	},
};

var chart = new ApexCharts(document.querySelector("#expenses1"), options);

chart.render();
