from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
import os, glob, random as rand, datetime

#from robotkitten.viewer.models import Comic

comic_root = os.path.join(os.path.dirname(__file__),"..","comics")
comic_root = os.path.normpath(comic_root)

def comic(request, comic_id=""):
  com = {}
  os.chdir(comic_root)

  if comic_id == "":
    tempcomics = os.listdir(comic_root)
    tempcomics.sort(reverse=True)

    for tmp in tempcomics:
      if glob.glob('%s/*.[pjg][npi][gf]' % tmp) != []:
        comic_id = tmp
        break

  comic_id = "%03d" % int(comic_id)

  try:
    file = glob.glob('%s/*.[pjg][npi][gf]' % comic_id)
    com['url'] = "/comics/%s" % file[0]
  except:
    raise Http404

  com['id'] = comic_id
  com['title'] = com['url'][12:-4]

  try:
    date = open("%s/date.txt" % comic_id).read().strip()
    com['date'] = datetime.datetime.strptime(date, "%Y-%m-%d")
  except:
    date = os.path.getmtime(file[0])
    com['date'] = datetime.datetime.fromtimestamp(date)

  #comic = Comic.objects.get(id=comic_id)
  try: com['alt'] = open("%s/alt.txt" % comic_id).read().strip()
  except: pass

  try: com['news'] = open("%s/news.txt" % comic_id).read()
  except: pass

  next = int(comic_id)+1
  try:
    file = glob.glob('%03d/*.[pjg][npi][gf]' % next)[0]
    com['next'] = "/%03d" % next
  except:
    pass

  prev = int(comic_id)-1
  try:
    file = glob.glob('%03d/*.[pjg][npi][gf]' % prev)[0]
    com['prev'] = "/%03d" % prev
  except:
    pass

  return render_to_response('comic.html', {'comic':com})

def random(request):
  tempcomics = os.listdir(comic_root)
  os.chdir(comic_root)
  comics = []

  for comic in tempcomics:
    try:
      file = glob.glob('%s/*.[pjg][npi][gf]' % comic)[0]
      comics.append(comic)
    except:
      pass

  r = rand.choice(comics)
  return HttpResponseRedirect("/%s" % r)
  

def list(request):
  os.chdir(comic_root)
  tempcomics = os.listdir(comic_root)
  tempcomics.sort(reverse=True)
  comics=[]

  for comic in tempcomics:
    try:
      file = glob.glob('%s/*.[pjg][npi][gf]' % comic)[0]
      title = "%s: %s" % (comic, file[4:-4])
      comics.append({'url':comic, 'title':title})
    except:
      pass

  return render_to_response('list.html', {'comics':comics})
