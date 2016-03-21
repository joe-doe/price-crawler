$( "#new_item" ).submit(function( event ) {
    var form_data= $(this).serializeArray();

    var record = {};
    var stores = [];
    var stores_data = JSON.parse(form_data[1].value);

    record["item_name"] = form_data[0].value;

    $.each(stores_data, function(k, v){
        var subrecord = {};
        subrecord["store_name"] = k;
        subrecord["url"] = v;
        stores.push(subrecord);
    });

    record["stores"] = stores;

    $.ajax({
            type: 'POST',
            url: 'store_item',
            data: JSON.stringify(record),
            contentType: 'application/json'
        })
        .done(function (data) {
            alert("OK");
        });

    event.preventDefault();
});