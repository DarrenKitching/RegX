import pyqrcode

def createQR(url):
	qr = pyqrcode.create(url)
	# qr.svg('uca-url.svg', scale=8)
	# qr.eps('uca-url.eps', scale=2)
	print(qr.terminal(quiet_zone=1))