# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect

def homepage(request):
    # Loads the designed hompag template in template folder
    t = loader.get_template('hompage.html')
    c = Context({
        
    })

    return HttpResponse(t.render(c))
    #return HttpResponse("Welcome to our homepage!")
