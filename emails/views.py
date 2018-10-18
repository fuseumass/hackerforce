from django.shortcuts import render


def emails(request):
    return render(request, 'emails.html.j2')


def drafts(request):
    return render(request, 'drafts.html.j2')


def sent(request):
    return render(request, 'sent.html.j2')


def outbox(request):
    return render(request, 'outbox.html.j2')
