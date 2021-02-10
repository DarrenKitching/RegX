import pyqrcode

def createQR(url):
	"""
	This function can turn a url into a QRCode image.

    Funciton makes it possible to produce a QRCode for our unique dose url's associated with each dose a patient is going to take.

    Args:
        url (string): url is a string of what our qr code should point to e.g. http://127.0.0.1:8000/dose/1z5Lff10AN

    Returns:
        print: Currently the function is only printing the qr code to the terminal and not saving them as images.

    """
	qr = pyqrcode.create(url)
	# qr.svg('uca-url.svg', scale=8)
	# qr.eps('uca-url.eps', scale=2)
	print(qr.terminal(quiet_zone=1))