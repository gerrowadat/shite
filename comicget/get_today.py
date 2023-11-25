import comicget

c = comicget.WebComic("Gunnerkrigg Court", "https://www.gunnerkrigg.com/")

print("Latest comic: %s" % (c.comic_img_url))
