$(document).ready(function() {
    $('#full_menu').DataTable( {

        responsive: true,

        scrollY:        '50vh',
        scrollCollapse: true,
        paging:         false,

        //dom: 'Bfrtip',

        "order": [[ 0, "desc" ]],


//        "columnDefs": [
  //          {
    //            "targets": [ 0 ],
      //          "visible": false,
        //        "searchable": true
          //  },
            //{
              //  "targets": [ 13 ],
                //"visible": false,
              //  "searchable": true
          //  }
      //  ]

    } );


} );
