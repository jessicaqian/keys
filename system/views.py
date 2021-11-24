from django.shortcuts import render

# Create your views here.

def main(request):

    if request.method == 'POST':
        pass

    else:
        pass
    return render(request, 'system/main.html',)

def configed(request):

    if request.method == 'POST':
        pass

    else:
        pass
    return render(request, 'system/configed.html',)

def free(request):

    if request.method == 'POST':
        pass

    else:
        pass
    return render(request, 'system/free.html',)