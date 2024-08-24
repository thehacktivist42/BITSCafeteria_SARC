from django.shortcuts import render
from django.http import HttpResponseRedirect
import sqlite3
db_conn = sqlite3.connect("test.db", check_same_thread=False)
cur = db_conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS ORDERS(NAME varchar(255), TOTAL integer)")
cartItems = 0
pageLoad = 0
total = 0
customerName = ''
menu = [
    {
        'name' : 'Masala Burger',
        'description' : 'A delightful fusion of traditional Indian spices with the classic burger format, featuring a flavorful patty made from spiced potatoes, chickpeas, or lentils, seasoned with a blend of aromatic spices.',
        'price' : 40,
        'added' : False,
        'quantity' : 0,
    },
    {
        'name' : 'French Fries',
        'description' : 'A timeless favorite: fresh, hand-cut potatoes fried to perfection, delivering a delightful crunch on the outside and a tender, fluffy interior.',
        'price' : 55,
        'added' : False,
        'quantity' : 0
    },
    {
        'name' : 'Choco Frappe',
        'description' : 'Dive into a blissful blend of rich chocolate and creamy goodness with our Choco Frappe. This indulgent treat combines smooth, velvety chocolate syrup with chilled, frothy milk and ice, all blended to a perfect consistency.',
        'price' : 55,
        'added' : False,
        'quantity' : 0
    },
    {
        'name' : 'Veg Sandwich',
        'description' : 'Savor the freshness of our Veg Sandwich, a wholesome and delicious choice for a light meal or snack. This sandwich features a medley of crisp, garden-fresh vegetables including lettuce, tomatoes, cucumbers, and shredded carrots, layered between slices of soft, toasted bread.',
        'price' : 50,
        'added' : False,
        'quantity' : 0
    },
    {
        'name' : 'Virgin Mojito',
        'description' : 'Refresh your senses with our Virgin Mojito, a non-alcoholic twist on the classic cocktail. This invigorating drink features a vibrant mix of muddled mint leaves and zesty lime, combined with a splash of sparkling soda for a fizzy finish. ',
        'price' : 70,
        'added' : False,
        'quantity' : 0
    },
    {
        'name' : 'Cheese Maggi',
        'description' : 'Indulge in our Cheese Maggi, a comforting twist on the classic noodle dish. This savory creation features tender, perfectly cooked Maggi noodles enveloped in a rich, creamy cheese sauce. ',
        'price' : 50,
        'added' : False,
        'quantity' : 0
    }
]
def home(request):
    for i in menu:
        i['amount'] = i['price']*i['quantity']
    global pageLoad
    global cartItems
    global total
    global customerName
    context = {
        'menu': menu,
        'cartItems' : cartItems,
        'pageLoad' : pageLoad,
        'total' : total,
        'customerName' : customerName
    }
    if request.method == 'GET':
        try:
            customerName = list(dict(request.GET).values())[1][0]
        except:
            pass
    if request.method == 'POST':
        name = list(request.POST.values())[1]
        for i in menu:
            if name in i['name']:
                i['added'] = True
                i['quantity'] += 1
                print(i['quantity'])
                cartItems+=1
                total += (i['quantity']*i['price'])
                return HttpResponseRedirect('/')
        if name == 'clear':
            cartItems = 0
            for i in menu:
                i['added'] = False
                i['quantity'] = 0
                total = 0
            return HttpResponseRedirect('/')
        if name == 'order':
            cur.execute(f"INSERT INTO ORDERS (NAME, TOTAL) VALUES('{customerName}', {total})")
            db_conn.commit()
            print([i for i in cur.execute("SELECT * FROM ORDERS")])
            return render(request, 'cafe/ordered.html', context)
    return render(request, 'cafe/home.html', context)

data = [i for i in cur.execute("SELECT * FROM ORDERS")]
data = [
        {
        'id' : data.index(i)+1,
        'name' : i[0],
        'total' : i[1]
        } for i in data
    ]
print(data)
def history(request):
    return render(request, 'cafe/history.html', context = {'cartItems' : 0, 'total' : 0, 'data' : data})