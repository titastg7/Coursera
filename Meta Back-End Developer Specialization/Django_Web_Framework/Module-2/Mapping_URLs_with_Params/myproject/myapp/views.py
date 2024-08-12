from django.shortcuts import render
from django.http import HttpResponse

def drinks(request, drink_name):
    drink = {
        'mocha' : 'type of coffee',
        'tea' : 'type of beverage',
        'lemonade' : 'type of refreshment',
        'hotchocolate' : 'type of winter drink'
    }
    choice_of_drink = drink[drink_name]
    return HttpResponse(f"<h2> {drink_name} </h2>" + f"<h3> {choice_of_drink} </h3>")
