import qrcode
# from app1 import usermail
usermail = "davidayadav694@gmail.com"
url = f"http://192.168.0.202:5000/register"
img = qrcode.make(url)
img.save(r"C:\Work\david\flask_qr_app\static\qr\register4.png")
print("QR code saved at static/qr/register4.png")
