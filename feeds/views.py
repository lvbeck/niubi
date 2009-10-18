from django.shortcuts import render_to_response

def latest_feed_proxy(request):
    return render_to_response('feeds/latest_proxy.html')

def hottest_feed_proxy(request):
    return render_to_response('feeds/hottest_proxy.html')