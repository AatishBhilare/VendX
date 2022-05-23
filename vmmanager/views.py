from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
import pyrebase
import time

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from upibasedvm import settings
from vmmanager.forms import EditVmItemForm
from vmmanager.models import VmItem, Transaction
from vmmanager.paytm import generate_checksum, verify_checksum


@login_required(login_url='login')
def index(request):
    vitems = VmItem.objects.all()

    invcount = VmItem.objects.filter(item_inv=0).count()
    context = {'vitems': vitems, 'invcount': invcount}
    return render(request, 'index.html', context)


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == 'POST':
            loginUsername = request.POST.get('loginUsername')
            loginPassword = request.POST.get('loginPassword')

            user = authenticate(request, username=loginUsername, password=loginPassword)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'username or password is incorrect')

        return render(request, 'login.html')


def logoutuser(request):
    logout(request)
    return redirect('login')


def edititem(request, itmid):
    invcount = VmItem.objects.filter(item_inv=0).count()
    vitems = VmItem.objects.all()
    vitem = VmItem.objects.get(id=itmid)
    form = EditVmItemForm(instance=vitem)

    if request.method == 'POST':
        form = EditVmItemForm(request.POST, request.FILES)
        if form.is_valid():
            newform = form.save(commit=False)
            vitem.item_name = newform.item_name
            vitem.item_price = newform.item_price
            vitem.item_inv = newform.item_inv
            if not newform.item_img == 'emptyfile':
                vitem.item_img = newform.item_img
            vitem.save()
            return redirect('edititem', vitem.id)
    context = {'vitem': vitem, 'form': form, 'vitems': vitems, 'invcount': invcount}
    return render(request, 'edit_item.html', context)


def initiate_payment(request, pitmid):
    if request.method == "GET":
        vitem = VmItem.objects.get(id=pitmid)
        context = {'vitem': vitem}
        return render(request, 'pay.html', context)
    try:
        item_id = request.POST['item_id']
        amount = float(request.POST['amount'])
        username = request.POST['username']
    except:
        return render(request, 'pay.html', context={'error': 'Wrong Accound Details or amount'})

    transaction = Transaction.objects.create(made_by=username, amount=amount, item_id=item_id)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    return render(request, 'redirect.html', context=paytm_params)


firebaseConfig = {
    'apiKey': "AIzaSyBxDhJoSLJ-lxG0Lr8AEcwCei60g33MBEI",
    'authDomain': "vendx-c11ee.firebaseapp.com",
    'projectId': "vendx-c11ee",
    'storageBucket': "vendx-c11ee.appspot.com",
    'messagingSenderId': "987254327724",
    'appId': "1:987254327724:web:0d76f5b0cfd756943c1209",
    'measurementId': "G-X255FRPV8L",
    'databaseURL': "https://vendx-c11ee-default-rtdb.firebaseio.com/"
}
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
database = firebase.database()


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        received_data = dict(request.POST)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            received_data['message'] = "Checksum Matched"
        else:
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'callback.html', context=received_data)
        oid = received_data['ORDERID'][0]
        tranobj = Transaction.objects.get(order_id=oid)
        if tranobj.item_id == 1:
            database.update({"Motor1": 'on'})
            time.sleep(2)
            database.update({"Motor1": 'off'})
        elif tranobj.item_id == 2:
            database.update({"Motor2": 'on'})
            time.sleep(2)
            database.update({"Motor2": 'off'})
        elif tranobj.item_id == 3:
            database.update({"Motor3": 'on'})
            time.sleep(2)
            database.update({"Motor3": 'off'})
        elif tranobj.item_id == 4:
            database.update({"Motor4": 'on'})
            time.sleep(2)
            database.update({"Motor4": 'off'})

        itmobj = VmItem.objects.get(id=tranobj.item_id)
        itmobj.item_inv = itmobj.item_inv - 1
        itmobj.save()

        return render(request, 'callback.html', context=received_data)


def home(request):
    vitems = VmItem.objects.all()

    context = {'vitems': vitems}
    return render(request, 'home.html', context)


# Get a database reference to our blog.

def sales(request):
    invcount = VmItem.objects.filter(item_inv=0).count()
    vitems = VmItem.objects.all()

    item1sc = Transaction.objects.filter(item_id=1).count()
    item2sc = Transaction.objects.filter(item_id=2).count()
    item3sc = Transaction.objects.filter(item_id=3).count()
    item4sc = Transaction.objects.filter(item_id=4).count()
    item1ta = 0
    item2ta = 0
    item3ta = 0
    item4ta = 0
    for vitem in vitems:
        if vitem.id == 1:
            item1ta = item1sc * vitem.item_price
        elif vitem.id == 2:
            item2ta = item2sc * vitem.item_price
        elif vitem.id == 3:
            item3ta = item3sc * vitem.item_price
        elif vitem.id == 4:
            item4ta = item4sc * vitem.item_price

    context = {'vitems': vitems,
               'item1sc': item1sc,
               'item2sc': item2sc,
               'item3sc': item3sc,
               'item4sc': item4sc,
               'item1ta': item1ta,
               'item2ta': item2ta,
               'item3ta': item3ta,
               'item4ta': item4ta,
               'invcount': invcount
               }
    return render(request, 'sales.html', context)
