var options = {
	series: [
		{
			name: "",
			data: [200, 330, 548, 740, 880, 1100],
		},
	],
	chart: {
		type: "bar",
		height: 210,
		toolbar: {
			show: false,
		},
	},
	dataLabels: {
		enabled: false,
	},
	plotOptions: {
		bar: {
			borderRadius: 0,
			horizontal: true,
			distributed: true,
			barHeight: "80%",
			isFunnel: true,
		},
	},
	colors: [
		"#d70000",
		"#ef0000",
		"#f11a1a",
		"#f23333",
		"#f44d4d",
		"#f56666",
		"#f78080",
		"#f99999",
	],
	dataLabels: {
		enabled: true,
		formatter: function (val, opt) {
			return opt.w.globals.labels[opt.dataPointIndex];
		},
		dropShadow: {
			enabled: true,
		},
	},
	xaxis: {
		categories: [
			"Grains",
			"Meat",
			"Dairy",
			"Processed Foods",
			"Healthy Fats",
			"Fruits & Vegetables",
		],
	},
	legend: {
		show: false,
	},
};

var chart = new ApexCharts(document.querySelector("#earnings"), options);
chart.render();
