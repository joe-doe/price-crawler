$( document ).ready(function() {

    var items = [];
    $.ajax({
        type: 'GET',
        url: 'get_items',
        async: false
        })
        .done(function (data){
            items = data;
        });

    var stores = []
    $.ajax({
        type: 'GET',
        url: 'get_stores',
        async: false
        })
        .done(function (data){
            stores = data;
        });



    for (var item in items) {
        var item_name = items[item];

        $.ajax({
           type: 'POST',
           url: 'get_specs_for_item',
           data: JSON.stringify({'item': item_name}),
           contentType: 'application/json',
           async: false
        })
        .done(function (res) {
            document.getElementById('chart_specs_'+item_name).innerHTML = res;
        });

        $.ajax({
           type: 'POST',
           url: 'get_quick_specs_for_item',
           data: JSON.stringify({'item': item_name}),
           contentType: 'application/json',
           async: false
        })
        .done(function (res) {
            document.getElementById('chart_quick_specs_'+item_name).innerHTML = res;
        });

        $.ajax({
           type: 'POST',
           url: 'get_image_for_item',
           data: JSON.stringify({'item': item_name}),
           contentType: 'application/json',
           async: false
        })
        .done(function (res) {
            $('#chart_image_'+item_name).attr('src', res);
            $('#chart_image_'+item_name).attr('width', '250px');
        });

        // chart labels
        var chart_labels = [];

        $.ajax({
            type: 'POST',
            url: 'get_timestamps_for_item',
            data: JSON.stringify({'item': item_name}),
            contentType: 'application/json',
            async: false
        })
        .done(function (data) {
            for (lab in data){
                human_date = moment(data[lab]*1000);
                chart_labels.push(human_date.format('LLL'));
            }
        });

        // chart datasets
        var chart_datasets = [];
        var stores = []

        $.ajax({
            type: 'POST',
            url: 'get_stores_for_item',
            data: JSON.stringify({'item': item_name}),
            contentType: 'application/json',
            async: false
        })
        .done(function (data) {
            stores = data;
        });

        for (store in stores) {
            $.ajax({
                type: 'POST',
                url: 'get_item_for_store',
                data: JSON.stringify({'item': item_name, 'store': stores[store]}),
                contentType: 'application/json',
                async: false
            })
            .done(function (res) {
                dataset_data = [];

                for (datum in res){
                    dataset_data.push(res[datum].price);
                }

                randomR = getRandomRGB();
                randomG = getRandomRGB();
                randomB = getRandomRGB();
                rgb = "rgba("+randomR+","+randomG+","+randomB+","

                dataset = {
                    label: stores[store],
                    datasetFill : false,
                    fillColor : rgb+"0)",
					strokeColor : rgb+"1)",
					pointColor : rgb+"1)",
					pointStrokeColor : "#fff",
					pointHighlightFill : "#fff",
					pointHighlightStroke : rgb+"1)",
                    data: dataset_data
                }

                chart_datasets.push(dataset);
//                console.log(dataset);
            });
        }

        // chart data
        var chart_data = {
            labels: chart_labels,
            datasets: chart_datasets
        }

        // get chart canvas
        var domItem = document.getElementById("chart_"+item_name).getContext("2d");

       // draw chart
       var myChart = new Chart(domItem).Line(chart_data,{
            responsive: true,
            multiTooltipTemplate: "<%= datasetLabel %> - <%= value %>",
            legendTemplate : "<ul class=\"legend <%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li style=\"color:<%=datasets[i].strokeColor%> !important; font-size: 1em;\"><span><%=datasets[i].value%>  <%if(datasets[i].label){%><%=datasets[i].label%><%}%></span></li><%}%></ul>",
            });

            document.getElementById('chart_legend_'+item_name).innerHTML = myChart.generateLegend();
    }

function getRandomRGB() {
  return Math.floor(Math.random() * (255 - 0 + 1)) + 0;
}
});