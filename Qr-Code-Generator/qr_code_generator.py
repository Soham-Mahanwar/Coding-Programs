import qrcode  

data = input("Enter the link: ").strip()  
filename = input("Enter the filename: ").strip()  

qr = qrcode.QRCode(box_size=10, border=4)  # Create a QRCode object
qr.add_data(data)  
qr.make(fit=True)  

image = qr.make_image(fill="black", back_color="white")  
image.save(f"{filename}.png")  

print(f"QR code generated with the name {filename}.png")  
