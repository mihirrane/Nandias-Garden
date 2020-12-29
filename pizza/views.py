from django.shortcuts import render
from django.forms import formset_factory
from django.urls import reverse
from .forms import PizzaForm, MultiplePizzaForm

def Home(request):
    return render(request, 'pizza/home.html')

def order(request):
    multiple_pizza_form = MultiplePizzaForm()
    if request.method == "POST":
        filled_form = PizzaForm(request.POST)   

        if filled_form.is_valid():
            note = "Thanks for ordering! Your %s %s and %s pizza is on its way!" %(filled_form.cleaned_data['size'], 
                                                                                filled_form.cleaned_data['topping1'],
                                                                                filled_form.cleaned_data['topping2'])
            new_form = PizzaForm()
            return render(request, 'pizza/order.html', {"pizzaform": new_form, "note" : note, "multiple_pizza_form": multiple_pizza_form})
    else:
        form = PizzaForm()
        return render(request, 'pizza/order.html', {"pizzaform" : form, "multiple_pizza_form": multiple_pizza_form})

def pizzas(request):
    if "number_of_pizzas" not in request.session:
        request.session["number_of_pizzas"] = 2
    filled_multiple_pizza_form = MultiplePizzaForm(request.GET)
    if filled_multiple_pizza_form.is_valid():
        request.session["number_of_pizzas"] = filled_multiple_pizza_form.cleaned_data['number']
    PizzaFormSet = formset_factory(PizzaForm, extra = request.session["number_of_pizzas"])
    formset = PizzaFormSet()
    if request.method == 'POST':
        filled_formset = PizzaFormSet(request.POST)
        if filled_formset.is_valid():
            # for form in filled_formset:
                # print(form.cleaned_data['topping1'])
            note = 'Your pizzas have been ordered'
            return render(request, 'pizza/order.html', {'note' : note})
        else:
            note = 'Your pizzas have not been ordered. Please try again!'   
        
            return render(request, 'pizza/pizzas.html', {'note' : note, 'formset' : formset})
    else:
        return render(request, 'pizza/pizzas.html', {'formset' : formset})