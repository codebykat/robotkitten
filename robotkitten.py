from flask import Flask, render_template, url_for, redirect, abort
app = Flask(__name__, static_url_path='' )
app.debug = True

import os, glob, random as rand, datetime

comic_root = os.path.join(os.path.dirname( __file__ ), "static/comics" )
comic_root = os.path.normpath( comic_root )

@app.route( "/" )
def home():
	tempcomics = os.listdir( comic_root )
	tempcomics.sort( reverse=True )

	for tmp in tempcomics:
		if glob.glob( '%s/%s/*.[pjg][npi][gf]' % ( comic_root, tmp ) ) != []:
			comic_id = tmp
			break

	return comic( tmp )

@app.route( "/<int:comic_id>" )
def comic( comic_id ):
	com = {}

	comic_id = "%03d" % int( comic_id )

	try:
		file = glob.glob( '%s/%s/*.[pjg][npi][gf]' % ( comic_root, comic_id ) )
		com['url'] = unicode(file[0][6:], "utf8")
		# com['url'] = url_for( 'static', filename=com['url'] )

	except:
		abort( 404 )

	com['id'] = comic_id
	com['title'] = unicode(file[0][18:-4], "utf8")

	try:
		date = open( "%s/%s/date.txt" % ( comic_root, comic_id ) ).read().strip()
		com['date'] = datetime.datetime.strptime( date, "%Y-%m-%d" )
	except:
		date = os.path.getmtime( file[0] )
		com['date'] = datetime.datetime.fromtimestamp( date )

	try: com['alt'] = open( "%s/%s/alt.txt" % ( comic_root, comic_id ) ).read().strip()
	except: pass

	try: com['news'] = open( "%s/%s/news.txt" % ( comic_root, comic_id ) ).read()
	except: pass

	next = int( comic_id ) + 1
	try:
		file = glob.glob( '%s/%03d/*.[pjg][npi][gf]' % ( comic_root, next ) )[0]
		com['next'] = "/%03d" % next
	except:
		pass

	prev = int(comic_id)-1
	try:
		file = glob.glob( '%s/%03d/*.[pjg][npi][gf]' % ( comic_root, prev ) )[0]
		com['prev'] = "/%03d" % prev
	except:
		pass

	return render_template( 'comic.html', comic=com )

@app.route( "/random" )
def random():
	tempcomics = os.listdir( comic_root )
	comics = []

	for comic in tempcomics:
		try:
			file = glob.glob( '%s/%s/*.[pjg][npi][gf]' % ( comic_root, comic ) )[0]
			comics.append( comic )
		except:
			pass

	r = rand.choice( comics )
	return redirect( url_for( 'comic', comic_id=r ) )

@app.route( "/list" )
def list():
	tempcomics = os.listdir( comic_root )
	tempcomics.sort( reverse=True )
	comics=[]

	for comic in tempcomics:
		try:
			file = glob.glob( '%s/%s/*.[pjg][npi][gf]' % ( comic_root, comic ) )[0]
			title = "%s: %s" % ( comic, file[len(comic_root)+5:-4] )
			title = unicode(title, "utf8")
			comics.append( {'url':unicode(comic, "utf8"), 'title':title} )
		except:
			pass

	return render_template( 'list.html', comics=comics )


## template filters ##
def datetimeformat( value, format='%H:%M / %d-%m-%Y' ):
    return value.strftime( format )
app.jinja_env.filters['datetimeformat'] = datetimeformat


if __name__ == "__main__":
	app.run()