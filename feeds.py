from django.contrib.syndication.feeds import Feed
import os, glob

comic_root = os.path.join(os.path.dirname(__file__),"comics")

class LatestComics(Feed):
  title = "robot+kitten"
  link = "/"
  description = "robot+kitten=?"

  def items(self):
    os.chdir(comic_root)
    tempcomics = os.listdir(comic_root)
    tempcomics.sort(reverse=True)
    comics=[]

    for comic in tempcomics:
      try:
        file = glob.glob('%s/*.[pjg][npi][gf]' % comic)[0]
        title = "%s: %s" % (comic, file[4:-4])
        news = ""
        try: news = open('%s/news.txt' % comic).read()
        except: pass
        alt = ""
        try: alt = open('%s/alt.txt' % comic).read()
        except: pass
        comics.append({'path':file, 'url':comic, 'title':title, 'news':news, 'alt':alt})
      except:
        pass

    return comics

  def item_link(self, item):
    return "http://robotkitten.net/%s" % item['url']
