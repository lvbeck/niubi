from django.shortcuts import render_to_response

def latest_feed_proxy(request):
    return render_to_response('latest_proxy.html')

def hottest_feed_proxy(request):
    return render_to_response('hottest_proxy.html')