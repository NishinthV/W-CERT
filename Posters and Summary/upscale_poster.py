from PIL import Image
import os

SRC = r"C:\Users\nishi\.gemini\antigravity\brain\99a9db68-b3e4-428d-a354-c889e7e597bb\wcert_poster_edited_1777921308737.png"
DST = r"c:\Users\nishi\OneDrive\Documents\Desktop\CSF\SEM8\Capestone\poster_final.png"

img = Image.open(SRC)
print(f"Source: {img.size}")

# A2 at 300 DPI = 4961 x 7016 (portrait)
A2_W, A2_H = 4961, 7016

# Scale image to fill A2 width, keep aspect ratio
scale = A2_W / img.width
new_h = int(img.height * scale)
img_resized = img.resize((A2_W, new_h), Image.LANCZOS)

# Create A2 canvas with dark background, center the image
canvas = Image.new("RGB", (A2_W, A2_H), (5, 5, 5))
y_offset = (A2_H - new_h) // 2
canvas.paste(img_resized, (0, y_offset))

# Save with 300 DPI metadata
canvas.save(DST, dpi=(300, 300))
fsize = os.path.getsize(DST)
print(f"Saved: {DST}")
print(f"Dimensions: {A2_W}x{A2_H} at 300 DPI")
print(f"File size: {fsize / (1024*1024):.1f} MB")
