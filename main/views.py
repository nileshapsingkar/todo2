from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse, response, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
# Create your views here.

def index(response, id):
    ls = ToDoList.objects.get(id=id)

    if ls in response.user.todolist.all():
        if response.method == "POST":
            if response.POST.get("save"):
                for item in ls.item_set.all():
                    if response.POST.get("c" + str(item.id)) == "clicked":
                        item.complete = True
                    else:
                        item.complete = False
                    item.save()
            
            elif response.POST.get("newItem"):
                txt = response.POST.get("new")

                if len(txt) > 2 :
                    ls.item_set.create(text = txt, complete = False)
                else:
                    print("invalid")
                #return render(response, "main/view.html", {})   
                return redirect("/view")

            if response.POST.get(ls.name):
                print(ls.name)
                ls.delete()
                return redirect("/view")

            for item in ls.item_set.all():
                if response.POST.get(item.text):
                    item.delete()
                    return redirect("/"+str(id))
                else:
                    print("invalid")
            
                

            
    return render(response, "main/list.html", {"ls" : ls})


def home(response):
    return render(response, "main/view.html", {})


def create(response):
   
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name = n)
            t.save()
            response.user.todolist.add(t)        

        return HttpResponseRedirect("/%i" %t.id)


    else:
        form = CreateNewList()

    return render(response, "main/create.html", {"form" : form})


def view(response):
    # todo = ToDoList.objects.get(id = id)   
    # if response.method == "POST" :
    #     if response.method.get(id):
    #         todo.delete()
    #         return render(response, "main/view.html", {})
    return render(response, "main/view.html", {})



def delete(response, id):
    todo = ToDoList.objects.get(id = id )
    if response.method == "POST":
        if response.POST.get():
            todo.item.delete(id)

        return redirect("/<int : id>/delete")
