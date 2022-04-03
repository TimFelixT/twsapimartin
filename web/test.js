
/*anychart.onDocumentReady(function () {
	// The data used in this sample can be obtained from the CDN
	// https://cdn.anychart.com/csv-data/csco-daily.js
	// create data table on loaded data
	//var container = document.getElementById("container");
	//stage = anychart.graphics.create("container");

	var dataTable = anychart.data.table();
	dataTable.addData(get_csco_daily_data());
	// map loaded data
	var mapping = dataTable.mapAs({"high": 1, "open": 2, "low": 3, "close": 4, "value": 4, "volume": 4});
	// create stock chart
	var chart = anychart.stock();

	// create plots on the chart
	var plot_0 = chart.plot(0);
	var plot_1 = chart.plot(1);
    var plot_2 = chart.plot(2);

	// create line series on both of them
	var ohlcSeries = plot_0.ohlc(mapping);
	ohlcSeries.name("CSCO OHLC");
	ohlcSeries.stroke("2px #64b5f6");

	// create a DMI indicator
	var dmi = plot_1.dmi(mapping);
    var dmi2 = plot_2.dmi(mapping,30,30,false,"spline","spline","spline")
	// set container id for the chart
	//chart.container(container);
	// initiate chart drawing
	chart.container('container');
	chart.draw();
	//stage.addChild(chart);

});
*/

function testo() {
	// The data used in this sample can be obtained from the CDN
	// https://cdn.anychart.com/csv-data/csco-daily.js
	// create data table on loaded data
	//var container = document.getElementById("container");
	//stage = anychart.graphics.create("container");

	var dataTable = anychart.data.table();
	dataTable.addData(get_csco_daily_data());
	// map loaded data
	var mapping = dataTable.mapAs({"high": 1, "open": 2, "low": 3, "close": 4, "value": 4, "volume": 4});
	// create stock chart
	var chart = anychart.stock();

	// create plots on the chart
	var plot_0 = chart.plot(0);
	var plot_1 = chart.plot(1);
    var plot_2 = chart.plot(2);

	// create line series on both of them
	var ohlcSeries = plot_0.ohlc(mapping);
	ohlcSeries.name("CSCO OHLC");
	ohlcSeries.stroke("2px #64b5f6");

	// create a DMI indicator
	var dmi = plot_1.dmi(mapping);
    var dmi2 = plot_2.dmi(mapping,30,30,false,"spline","spline","spline")
	var pdi_test = dmi2.pdiSeries();
	var adx_test = dmi2.adxSeries();
	var ndi_test= dmi2.ndiSeries();
	var datatest = ndi_test.data(); 
	var indest_test = ndi_test.getIndex();
	//var test = dmi2.get(9)
	// set container id for the chart
	//chart.container(container);
	// initiate chart drawing
	var test = pdi_test[0];

	var da = pdi_test.getDataValue("value");
	chart.container('container');
	chart.draw();
	//stage.addChild(chart);

};

testo();