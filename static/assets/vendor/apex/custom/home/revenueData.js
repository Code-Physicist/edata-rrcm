var options = {
	chart: {
		height: 219,
		type: "bar",
		toolbar: {
			show: false,
		},
	},
	plotOptions: {
		bar: {
			horizontal: false,
			columnWidth: "40px",
			distributed: true,
			borderRadius: 2,
		},
	},
	dataLabels: {
		enabled: false,
	},
	stroke: {
		show: true,
		width: 1,
		colors: ["#e50000", "#006be5", "#008d02", "#ffca28"],
	},
	series: [
		{
			name: "New",
			data: [5000, 4000, 3000, 2000],
		},
	],
	legend: {
		show: false,
	},
	xaxis: {
		categories: ["Sales", "Visits", "Income", "Revenue"],
	},
	yaxis: {
		show: false,
	},
	fill: {
		opacity: 1,
	},
	tooltip: {
		y: {
			formatter: function (val) {
				return +val;
			},
		},
	},
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
			left: 0,
		},
	},
	colors: ["#e50000", "#006be5", "#008d02", "#ffca28"],
};
var chart = new ApexCharts(document.querySelector("#revenueData"), options);
chart.render();
