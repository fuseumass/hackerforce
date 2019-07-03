from django.shortcuts import render

# Create your views here.
def emails(request):
  return render(request, "email_compose.html")