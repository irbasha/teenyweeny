from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import TeenyURLs

import urllib
import hashlib


def index(request):
	return render(request, "teeny/index.html")


def createurl(request):
	url = request.GET['url']
	hashObject = hashlib.md5(url.encode())
	shortened_url_hash = hashObject.hexdigest()[:8]

	try:
		check_url_exists = TeenyURLs.objects.get(teeny_url=shortened_url_hash)
	except TeenyURLs.DoesNotExist:
		entry = TeenyURLs(teeny_url=shortened_url_hash, origin_url=url)
		entry.save()

	shortened_url = convertURLFromCode(shortened_url_hash)
	return render(request, 'teeny/index.html', {'shortened_url': shortened_url})


def retrieve(request, inputURL):
	target = get_object_or_404(TeenyURLs, teeny_url=inputURL)
	targetURL = target.origin_url
	return redirect(targetURL)


def convertURLFromCode(code):
    return 'http://localhost:8000/%s' % (code)
