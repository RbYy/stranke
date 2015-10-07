from django.http import HttpResponseRedirect
from django.shortcuts import render
from stranke4.models import *
from django.utils import timezone
from django.http import HttpResponse
from django import forms
from datetime import datetime
from django.db.models import Q
import json
from django.core import serializers
from django.db.models import Max, Sum
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator
from registration.backends.default.views import RegistrationView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from bootstrap3_datepicker.widgets import DatePickerInput
from decimal import Decimal
from django.core.urlresolvers import reverse



vsi_produkti = [a.okrajsava for a in Produkt.objects.all()]

        

class MyRegistrationiew(RegistrationView):
    def get(self, request, *args, **kwargs):
        context=super().get(request)
        print (context)
        
    
class StrankaForm(forms.Form):
    podjetje = forms.CharField(max_length=100)
    naslov = forms.CharField(max_length=100)
    kraj = forms.CharField(max_length=30)
    oseba = forms.CharField(max_length=100)


class ObiskForm(forms.Form): 
    datum = forms.DateField(widget=DatePickerInput(format="%Y-%m-%d",
                                                   options={"language": "sl"}))
    prodaja = forms.CharField(max_length=200, required=False)
    demo = forms.CharField(max_length=200, required=False)
    znesek = forms.DecimalField(initial=0, max_digits=8, decimal_places=2)

class ProduktForm(forms.Form):
    ime = forms.CharField(max_length=30)
    okrajsava = forms.CharField(max_length=5)



@login_required  
def dodaj_produkt(request): 
    p=Produkt.objects.all()
    if request.method == 'POST':
        form = ProduktForm(request.POST)
        print(request.POST)
        print(request.POST['ime'])
        
        if form.is_valid():
            print(form.cleaned_data['ime'])
            Produkt.objects.create(
                                   ime=form.cleaned_data['ime'],
                                   okrajsava=form.cleaned_data['okrajsava'])           
        else:
            HttpResponse('popravi vnos!')
    else:
        form=ProduktForm()
    if 'count' in request.session:
        request.session['count'] += 1
    else:
        request.session['count'] = 1
    return render(request, 'polls/produkti.html', {'p':p,
                                                       'form':form,
                                                       'count':request.session['count'],
                                                       })
                

@login_required
def pokazi_listo(request):
    #print(request)
    if request.method == 'GET':
        stran=int(request.GET.get('stran'))
        if 'brisi' in request.GET:
            if request.GET['brisi'] !='':
                brisi_pk= int(request.GET['brisi'])
                Stranka.objects.get(pk=brisi_pk).delete()
        if 'produkti' in request.GET:
            produkti = request.GET['produkti']
        if 'filter' in request.GET:
            vnos=request.GET['filter'] #po prometu
        if 'naziv' in request.GET:
            naziv = request.GET['naziv'] #po nazivu podjetja
    res=Stranka.objects.filter(uporabnik= request.user).annotate(datum_max=Max('obisk__datum')).order_by('-skupaj_prodano')
    if vnos !='':#g
        if vnos[0] == '0':
            res= res.filter(skupaj_prodano__lte = float(vnos[1:])).annotate(datum_max=Max('obisk__datum')).order_by('-skupaj_prodano')
        else:
            res= res.filter(skupaj_prodano__gte = float(vnos)).annotate(datum_max=Max('obisk__datum')).order_by('-skupaj_prodano')   
    if naziv:
        res= res.filter(Q(podjetje__icontains = naziv) | Q(kraj__icontains = naziv)).annotate(datum_max=Max('obisk__datum')).order_by('-skupaj_prodano')       
    if produkti:
        produkti=produkti.upper().split(' ')
        for i in produkti:
            if i in vsi_produkti:
                res = res.filter(produkt__okrajsava=i)
    
    lista_zneskov_podniza_strank=[]
    stevilo_obiskov_podniza_strank=0
    povprecna_zakljucnica=" "
    promet=" "
    stevilo_strank=" "
    stevilo_vnosov=" "
    
    if res:
        print("dsfsdfsdf")
        for stranka in res:
            obiski_pri_stranki=Obisk.objects.filter(stranka=stranka)
            zneski_pri_stranki=[obisk.znesek for obisk in obiski_pri_stranki if obisk.znesek>0]
            stevilo_obiskov_podniza_strank+=len(zneski_pri_stranki)        
            for i in zneski_pri_stranki:
                lista_zneskov_podniza_strank.append(i)
        if stevilo_obiskov_podniza_strank > 0:
            povprecna_zakljucnica=round(sum(lista_zneskov_podniza_strank)/stevilo_obiskov_podniza_strank,2)
        else:
            povprecna_zakljucnica=0    
        promet=res.aggregate(promet=Sum('skupaj_prodano'))
        stevilo_strank= res.filter(skupaj_prodano__gt=0).count()
        p = Paginator(res, 10)
        
        data = serializers.serialize('json', p.page(stran))
        struct=json.loads(data) 
        i=0
        for j in p.page(stran):
            struct[i]['fields']['datum_max'] = j.datum_max   
            i+=1 
        promet=promet['promet']
        stevilo_vnosov=res.count()   
    else:
        struct=[]    
    struct.append({'stevilo_vnosov':stevilo_vnosov,
                   'stevilo_strank':stevilo_strank,
                   'promet':promet,
                   'povprecna_zakljucnica':povprecna_zakljucnica})
    data = json.dumps(struct, cls=DjangoJSONEncoder)
    #print(HttpResponse(data).content.decode())
    req=dict((key.lstrip('HTTP_'),value) for (key, value) in request.META.items() if key.startswith('HTTP_'))
    for key, value in req.items():
        print(key,' : ',value)
    return HttpResponse(data)
   
def redirekt(request):
    return HttpResponseRedirect(reverse('stranke4:stranke'))
@login_required
def stranke(request):
    stevilo_vnosov= Stranka.objects.filter(uporabnik=request.user).count()
    stevilo_strank= Stranka.objects.filter(uporabnik=request.user).filter(skupaj_prodano__gt=0).count()
    
    if request.method == 'POST': 
        form = StrankaForm(request.POST) 
        if form.is_valid(): 
            Stranka.objects.create(
                                   podjetje=form.cleaned_data['podjetje'],
                                   naslov=form.cleaned_data['naslov'],
                                   kraj=form.cleaned_data['kraj'],
                                   oseba=form.cleaned_data['oseba'],
                                   skupaj_prodano = 0,
                                   uporabnik=request.user,
                                   )
            return HttpResponseRedirect(reverse('stranke4:stranke', current_app=request.resolver_match.namespace)) 
    else:
        form = StrankaForm() 
    return render(request, 'polls/stranke.html', {'form':form,
                                                  'stevilo_vnosov':stevilo_vnosov,
                                                  'stevilo_strank':stevilo_strank})


@login_required
def obiski_med_datumoma(request, stranka_id):
    try:
        
        zacetni_datum=request.GET['zacetek']
        koncni_datum=request.GET['konec']
    except:
        zacetni_datum=''
        koncni_datum=''
    #if request.method == 'GET':
    if 'zacetek' and 'konec' in request.GET.keys():
        if request.GET['zacetek'] and request.GET['konec']:
            zacetni_datum=request.GET['zacetek']
            koncni_datum=request.GET['konec']
            res= Obisk.objects.filter(stranka__id=stranka_id, datum__gte=zacetni_datum, datum__lte=koncni_datum)
        elif request.GET['zacetek'] and not request.GET['konec']:
            zacetni_datum=request.GET['zacetek']
            res= Obisk.objects.filter(stranka__id=stranka_id, datum__gte=zacetni_datum)
        elif request.GET['konec'] and not request.GET['zacetek']:
            koncni_datum=request.GET['konec']
            res= Obisk.objects.filter(stranka__id=stranka_id, datum__lte=koncni_datum)
        else:
            res= Obisk.objects.filter(stranka__id=stranka_id)
        return res
    else:
        res= Obisk.objects.filter(stranka__id=stranka_id).order_by('-datum')
        return res

@login_required
def filtriraj_obiske(request, stranka_id):
    print(request.user)
    if request.user != 'robertb':
        manager=Produkt.objectsss
        print('manager', manager.zacne('X'))
    else:
        manager=Produkt.objects
        
        print('doto')
        print('manager', manager.all())
    zacetek = datetime.now()
    respo = obiski_med_datumoma(request, stranka_id).order_by('-datum')
    if 'brisi' in request.GET:
        if request.GET['brisi'] !='':
            brisi_pk= int(request.GET['brisi'])
            Obisk.objects.get(pk=brisi_pk).delete()
            novaVsota=Obisk.objects.filter(stranka_id=stranka_id).aggregate(nova=Sum('znesek'))
            stranka=Stranka.objects.get(id=stranka_id)
            stranka.skupaj_prodano=novaVsota['nova']
            stranka.save()

    try:
        stran = int(request.GET["stran"])
        zahteva=request.GET["filter"]
    except:
        stran=1
        zahteva=''
   
    vnos=zahteva.upper().split()
    stevila, besede, stevilaEX, besedeEX = [], [], [], []
    for i in vnos:
        if i[0]=='*':
            try:
                stevilaEX.append(float(i[1:]))
            except:
                besedeEX.append(i[1:])
        else:
            try:
                stevila.append(float(i))
            except:
                besede.append(i)
    
    if stevila:
        respo = respo.filter(znesek__gte = stevila[0]).order_by('-datum')
    if stevilaEX:
        respo = respo.filter(znesek__lte = stevilaEX[0]).order_by('-datum')
    if besede:
        for i in besede:
            if i in vsi_produkti:
                respo = respo.filter(prodaja__okrajsava=i).order_by('-datum')
    if besedeEX:
        for i in besedeEX:
            if i in vsi_produkti:
                respo = respo.exclude(prodaja__okrajsava=i).order_by('-datum')            
    try:
        nova_vsota=respo.aggregate(nova_vsota=Sum('znesek'))
    except:
        nova_vsota=0
    p= Paginator(respo, 10)
    print('nova vsota',nova_vsota)
    data = serializers.serialize('json', p.page(stran), use_natural_keys=True)
    struct=json.loads(data)
    struct.append({'stevilo':respo.count()})
    struct.append(nova_vsota)
         
    data=json.dumps(struct, cls=DjangoJSONEncoder)
    cas = datetime.now()-zacetek
    print('trajanje: ', cas)
    return HttpResponse(data)
    # da vidimo ali git opazi to
    

@login_required
def pokazi_skladisce(request):
    stranka_id=int(request.GET['stranka_id'])
    a= Produkt.objects.filter(skladisce=stranka_id)
    data=''
    for s in a: data+= s.okrajsava+' '
    return HttpResponse(data)  
    

def validacija(request, stranka_id):
    prodaje= request.GET['vnosP'].split()
    demoti = request.GET['vnosD'].split()
    vnosi = prodaje+demoti
    for i in vnosi:
        if not i in vsi_produkti:   
            return HttpResponse("napaka")
    return HttpResponse("ok")
   

@login_required
def stranka(request, stranka_id):        
    p=Stranka.objects.get(id=stranka_id)
    if request.method == 'GET':
        form = ObiskForm(request.GET)
        if form.is_valid():
            #from decimal import *
            prodaje = form.cleaned_data['prodaja'].upper().split()
            demoti = form.cleaned_data['demo'].upper().split()
            p.skupaj_prodano=Decimal(p.skupaj_prodano)+Decimal(float(form.cleaned_data['znesek']))
            p.save()
            obisk=Obisk.objects.create(
                                 datum=form.cleaned_data['datum'],
                                 znesek=form.cleaned_data['znesek'],
                                 stranka=Stranka.objects.get(id=stranka_id)
                                 )
            for i in prodaje: #zapolni m2m polja
                produkt=Produkt.objects.get(okrajsava=i)
                obisk.prodaja.add(produkt) 
                produkt.skladisce.add(p)
            for i in demoti:
                produkt=Produkt.objects.get(okrajsava=i) 
                obisk.demo.add(produkt)
            #return HttpResponseRedirect(reverse('stranka', args=(stranka_id,)))
            filtriraj_obiske(request, stranka_id)
    else:
        form = ObiskForm()
        
    # oblakci z napisi navodili in namigi
    oblak_filter = 'V polje vnesi okrajsave produktov locene s presledkom za prikaz obiskov, kjer si te produkte prodal. Vnesi znesek za prikaz obiskov s prometom nad dolocenim zneskom. Vnesi znesek z zvezdico spredaj (npr: *250) za prikaz obiskov s prometom nizjim od vnosa. Podobno, zvezdica pred produktom (npr: *rbx) prikaze le obiske, kjer ni prodaje vnesenega produkta. Primer: vnos "100 aq rbx *300" prikaze obiske, kjer sta bila prodana vsaj RBX in AQ v znesku med 100 in 300 eur'
    return render(request, 'polls/stranka.html', {'p':p,
                                                  'form':form,
                                                  'stranka_id':stranka_id,
                                                  'oblak_filter':oblak_filter})
    


@login_required
def odjava(*args, **kwargs):
    logout(args[0])
    return HttpResponseRedirect('/accounts/login/')