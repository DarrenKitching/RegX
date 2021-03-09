import pyqrcode

def createQR(videoURL):
	"""
	This function can turn a url into a QRCode image.

    Funciton makes it possible to produce a QRCode for our unique dose url's associated with each dose a patient is going to take.

    Args:
        url (string): url is a string of what our qr code should point to e.g. http://127.0.0.1:8000/dose/1z5Lff10AN

    Returns:

    """
	qr = pyqrcode.create('http://127.0.0.1:8000/' + videoURL)
	qr.svg('media/QR-Codes/' + videoURL + '.svg', scale=4)