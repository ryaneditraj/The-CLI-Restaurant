no = int(input("Product no>"))
product = input("product name>")
product_code = input("Product code>")




template = f"""
if option == {no}:
        print("{product} coming up")
        {product_code}_no = str(input("How Many: "))
        items = (hitems+","+"{product} "+{product_code}_no)
        print(items)
        hitems = items"""
print(template)


