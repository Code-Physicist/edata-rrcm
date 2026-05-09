var options = {
	series: [
		{
			name: "Sales",
			type: "area",
			data: [200, 370, 50, 250, 650, 150, 400],
		},
		{
			name: "Income",
			type: "line",
			data: [230, 400, 80, 280, 680, 180, 430],
		},
	],
	chart: {
		height: 320,
		type: "area",
		zoom: {
			enabled: false,
		},
		toolbar: {
			show: false,
		},
	},
	stroke: {
		width: [0, 4],
		curve: "smooth",
	},
	dataLabels: {
		enabled: true,
		enabledOnSeries: [1],
	},
	labels: [
		"Sunday",
		"Monday",
		"Tuesday",
		"Wednesday",
		"Thursday",
		"Friday",
		"Saturday",
	],
	grid: {
		borderColor: "#ccd2da",
		strokeDashArray: 3,
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
			bottom: 0,
			left: 30,
		},
	},
	colors: ["#ffecec", "#ef0000"],
	xaxis: {
		type: "day",
	},
};

var chart = new ApexCharts(document.querySelector("#salesIncome"), options);
chart.render();
