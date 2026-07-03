import pymupdf

doc = pymupdf.open("data\Advanced_Business_Seller_Guide_May09.pdf")
data = []
for page in doc:
    # print(page.get_text())
    data.append(page.get_text())
    # data.append(f"{page.get_text()}")
    # data.append(",")

print(data)

