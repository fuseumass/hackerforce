from django.shortcuts import render


def emails(request):
    return render(request, 'emails.html')


def drafts(request):
    return render(request, 'drafts.html')


def sent(request):
    return render(request, 'sent.html')


def outbox(request):
    return render(request, 'outbox.html')
