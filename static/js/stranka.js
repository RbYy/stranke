var query='';
var query2='';
var naziv='';
var stran = 1;
var brisi ='';


function zapolni(stran, query, query2, naziv, brisi){

    $.getJSON(pokazi_listo, {stran:stran, 
                                 filter:query, 
                                 produkti:query2, 
                                 naziv:naziv, 
                                 brisi:brisi}, function(data){
        var stevilke_strani='';
        $('.stran').remove();
        $('.vrstica').remove();
        $('.skladisce_vse').remove();
        console.log("ddddddd");
        if (data.length > 1) {
            for (var i=1; i < Math.ceil(data[data.length-1]['stevilo_vnosov']/10)+1; i++){
                stevilke_strani+='<span class="stran" id="stran'+i+'"> '+i+' </span>';
            }
            $('caption').append(stevilke_strani);
         }
        var vsebina_tabele = '';
        for (var i=0; i < data.length-1; i++){
            vsebina_tabele += ('<tr class="vrstica warning" id="'+data[i]['pk']+'"><td class="naziv"><a href="./stranka/'+data[i]['pk']+'/">'+ data[i]["fields"]["podjetje"] + '</a></td><td class="kraj">'
            + data[i]["fields"]["kraj"] +'</td><td class="vsota">'+ data[i]['fields']["skupaj_prodano"] +'</td><td class="zadnji_datum" style="text-align:right">'+ data[i]['fields']["datum_max"]+'</td>');
            vsebina_tabele += '<td class="brisi"><button type="button" data-target="#brisiModal" class="btn btn-default btn-xs" id="' + data[i]["pk"] +'" aria-label="Left Align"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td></tr>';
         }
        console.log(data);
        $('tbody').append(vsebina_tabele);
        $('.stevilo_vnosov').text(data[data.length-1]['stevilo_vnosov']);
        $('.stevilo_strank').text(data[data.length-1]['stevilo_strank']);
        $('.promet').text(data[data.length-1]['promet']);
        $('.povp_zaklj').text(data[data.length-1]['povprecna_zakljucnica'])


     });
}



/* preveri ali so vnosna polja izpolnjena */
if ($('#po_nazivu').val()){
    naziv = $('#po_nazivu').val();
}
if ($('#po_produktih').val()){
    query2 = $('#po_produktih').val();
}
if ($('#suggestion').val()){
    query = $('#suggestion').val();
}


zapolni(stran , query, query2, naziv, brisi); /* zacetno zapolnjevanje tabele (ob osvezevanju strani) */


$('#suggestion').keyup(function(){ /* filtriraj po prometu */
    query = $(this).val();
    zapolni(stran, query, query2, naziv, brisi);
});

$('#po_produktih').keyup(function(){ /* filtriraj po produktih */
    query2 = $(this).val();
    zapolni(stran, query, query2, naziv, brisi);
});

$('#po_nazivu').keyup(function(){ /* filtriraj po nazivu */
    naziv = $(this).val();
    zapolni(stran, query, query2, naziv, brisi);
});

$(".container").on('click', '.vrstica', function(){ /* pokazi podrobnosti */
    var vrstica_id = $(this).attr('id');
    $.get('/pokazi_skladisce/', {stranka_id : vrstica_id}, function(data){
        $('.skladisce_vse').remove();
        $('<tr class="skladisce_vse"><td colspan="5">'+data+'</td></tr>').insertAfter('#'+vrstica_id);
     });
});

$('.container').on('click', '.stran', function(){ /*obrni stran*/
       var stran=$(this).text();
       zapolni(stran, query, query2, naziv, brisi);
});
$('.container').on('click', '.btn-xs', function(){
    var brisi=$(this).attr('id');
    
    $('#brisiModal').modal('show');
    console.log('doto');
    $('#brisiModal').on('click', '#brisi', function(){ /* zbriši stranko iz baze */
        $('#brisiModal').modal('hide');
        zapolni(stran, query, query2, naziv, brisi);
        
    });
});    