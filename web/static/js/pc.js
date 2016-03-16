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
                chart_labels.push(human_date.format('lll'));
            }
        });

        // chart datasets
        var chart_datasets = [];
        var stores = []

        $.ajax({
            type: 'GET',
            url: 'get_stores',
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
                    fillColor : rgb+"0.1)",
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

            });
    }

function getRandomRGB() {
  return Math.floor(Math.random() * (255 - 0 + 1)) + 0;
}
//    $.post('');

//   var barData = {
//   labels : [{% for item in labels %}
//                  "{{item}}",
//              {% endfor %}],
//   datasets : [
//      {
//            fillColor: "rgba(151,187,205,0.2)",
//            strokeColor: "rgba(151,187,205,1)",
//            pointColor: "rgba(151,187,205,1)",
//         data : [{% for item in values %}
//                      {{item}},
//                    {% endfor %}]
//      }
//      ]
//   }
//   // get bar chart canvas
//   var mychart = document.getElementById("chart").getContext("2d");
//   steps = 10
//   max = 10
//   // draw bar chart
//   new Chart(mychart).Bar(barData, {
//        scaleOverride: true,
//        scaleSteps: steps,
//        scaleStepWidth: Math.ceil(max / steps),
//        scaleStartValue: 0,
//        scaleShowVerticalLines: true,
//        scaleShowGridLines : true,
//        barShowStroke : true,
//        scaleShowLabels: true
//   });
});