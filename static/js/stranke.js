var zahteva ='';
//var zacetni_datum = '2000-01-01';
//var koncni_datum= new Date();
//var dd = koncni_datum.getDate();
//var mm = koncni_datum.getMonth()+1; //januar je 0!
//var yyyy = koncni_datum.getFullYear();
//if(dd<10) { dd='0'+dd; } 
//if( mm<10 ) { mm='0'+mm; } 
//koncni_datum = yyyy+'-'+mm+'-'+dd;
var zacetni_datum = '';
var koncni_datum='';
//var pot = /filtriraj_obiske/ + stranka_id;
var stran = 1;
var brisi = '';
console.log(pot);
function zapolniObiske(pot, zahteva, zacetni_datum, koncni_datum, stran, brisi){
        var vsebina = '';
        $.getJSON(pot, {filter:zahteva, 
                        zacetek:zacetni_datum, 
                        konec:koncni_datum, 
                        stran:stran,
                        brisi:brisi}, 
                        function(data){
             $('.stran').remove();
             $('.vrs').remove();
             $('.vsota').remove();
             stevilke_strani='';
            console.log(zacetni_datum, koncni_datum);
            console.log(data);
            if (data.length > 0) {
                for (var i=1; i < Math.ceil(data[data.length-2]['stevilo']/10)+1; i++){
                    stevilke_strani+='<span class="stran" id="stran'+i+'"> '+i+' </span>';
                }
            }
                $('.strani').append(stevilke_strani);
            for (var i = 0; i < data.length-2; i++){
                vsebina += '<tr class="vrs warning"><td class="datum">' +data[i]['fields']['datum']+'</td>';
                vsebina += '<td class="demo">' +data[i]['fields']['demo']+'</td>';
                vsebina += '<td class="prodaja">' +data[i]['fields']['prodaja']+'</td>';
                vsebina += '<td class="znesek" style="text-align:right">' +data[i]['fields']['znesek'];
                vsebina += '<td class="brisi"><button type="button" data-target="#brisiModal" style="text-align:right" class="btn btn-default btn-xs" id="' + data[i]["pk"] +'" aria-label="Left Align"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button></td></tr>';
                }
            vsebina += '<tr class="vsota"><td></td><td></td><td></td><td style="text-align:right;" id="vsota">'+ data[data.length-1]['nova_vsota'] +'</td><td></td></tr>';
            $('tbody').append(vsebina);   
                
        });  
}
zapolniObiske(pot, zahteva, zacetni_datum, koncni_datum,stran, brisi);

$("#fil").keyup(function(){
    zahteva = $(this).val();
    //var pot = /filtriraj_obiske/ + stranka_id;
    zapolniObiske(pot, zahteva, zacetni_datum, koncni_datum, stran, brisi);
});


$('.input-daterange').datepicker({
        format:'yyyy-mm-dd',
        autoclose:'rue',
        language:"sl",
        }).on('changeDate',function(zacetni,koncni){
                            zacetni_datum = $('#startDate').val();
                            koncni_datum = $('#endDate').val();
                            zapolniObiske(pot, zahteva, zacetni_datum, koncni_datum, stran, brisi);
                            }
        );
        
$('.container').on('click', '.stran', function(){ /*obrni stran*/
       stran=$(this).text();
       zapolniObiske(pot, zahteva, zacetni_datum, koncni_datum, stran, brisi); 
});

$('.container').on('click', '.btn-xs', function(){
    var brisi=$(this).attr('id');
    $('#brisiModal').modal('show');
    $('#brisiModal').on('click', '#brisi', function(){ /* zbriši stranko iz baze */
        $('#brisiModal').modal('hide');
        zapolniObiske(pot, zahteva, zacetni_datum, koncni_datum, stran, brisi);
        
    });
});


$('#forma').submit(function(event){ /* preveri ali so vneseni produkti veljavni */
    event.preventDefault();
    $('.napaka').remove();
    $('.modal-footer').prepend('<spam class="napaka" style="color:red;"></spam>');
    var vnosP = $('#id_prodaja').val();
    var vnosD = $('#id_demo').val();
    var pot1='/validacija/' + stranka_id;
    
    $.get(pot1, {vnosP:vnosP, vnosD:vnosD}, function(data){
            if (data == "napaka"){
                $('.napaka').text('eden ali več neveljavnih produktov');
            }            
            else {
               $('#myModal').modal('hide');
               $('#forma').unbind().submit();
            }                        
    });
});
