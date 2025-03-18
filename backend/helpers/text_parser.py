import re

# ฟังก์ชันแปลงข้อความที่ดึงจากใบเสร็จเป็นโครงสร้าง JSON
def parse_extracted_text(text):
    cleaned_text = text.replace("*", "").strip()
    lines = cleaned_text.split("\n")

    store_name = re.search(r"Store name:\s*(.+)", cleaned_text) or re.search(r"Store Name:\s*(.+)", cleaned_text) or re.search(r"store name:\s*(.+)", cleaned_text)
    date_time = re.search(r"Date:\s*(.+)", cleaned_text) or re.search(r"date:\s*(.+)", cleaned_text)
    receipt_number = re.search(r"Receipt number:\s*(.+)", cleaned_text) or re.search(r"Receipt Number:\s*(.+)", cleaned_text)


    # vat = (
    # re.search(r"vat:\s*(.+)", cleaned_text) or
    # re.search(r"Vat:\s*(.+)", cleaned_text) or
    # re.search(r"VAT:\s*(.+)", cleaned_text))

    vat = (
    re.search(r"vat:\s*\$?([\d,]+(\.\d+)?)", cleaned_text, re.IGNORECASE) or
    re.search(r"Vat:\s*\$?([\d,]+(\.\d+)?)", cleaned_text, re.IGNORECASE) or
    re.search(r"VAT:\s*\$?([\d,]+(\.\d+)?)", cleaned_text, re.IGNORECASE))

    # vat = int(match.group(1)) if match else 0 

    # total = re.search(r"total:\s*(.+)", cleaned_text) or re.search(r"Total:\s*(.+)", cleaned_text)
    total = (
    re.search(r"total:\s*\$?([\d,]+(\.\d+)?)", cleaned_text, re.IGNORECASE) or
    re.search(r"Total:\s*\$?([\d,]+(\.\d+)?)", cleaned_text, re.IGNORECASE))


    parsed_data = {
        "store_name": store_name.group(1).strip() if store_name else "",
        "date_time": date_time.group(1).strip() if date_time else "",
        "receipt_number": receipt_number.group(1).strip() if receipt_number else "",
        "items": [],
        "vat" : vat.group(1) if vat else "0",
        # vatc_cond = vat if vat.replace(".", "", 1).isdigit() else "0"

        "total" : total.group(1) if total else "0",
        "raw_text" : cleaned_text

    }
    

    for line in lines:
        # Define patterns for matching
        patterns = [
            r"([^:]+):\s*(\d+)\s*x\s*\$?([\d,]+\.\d{2})",  # ✅ จับ "Services: 10 x $55.00"
            r"([^:]+):\s*\$?([\d,]+\.\d{2})",              # ✅ จับ "Product: $120.50" (ราคาอย่างเดียว)
            r"([^:]+)\s+(\d+)\s*x\s*\$?([\d,]+\.\d{2})",   # ✅ จับ "Product 5 x $120.50" (ไม่มี :)
            r"([^:]+):\s*(\d+\.\d+)\s*x\s*\$?([\d,]+\.\d{2})",  # ✅ จับ "Item: 2.5 x 10.00"
            r"([^:]+)\s*x\s*\$?([\d,]+\.\d{2})",           # ✅ จับ "Service x $55.00" (ไม่มีจำนวน)
            r"\|([^|]+)\|\s*(\d+)\s*\|\s*\$?([\d,]+\.\d{2})\s*\|\s*\$?([\d,]+\.\d{2})\s*\|", # ✅ จับ "| น้ำแข็ง | 2 | 15.00 | 30.00 |"
            r"([^-:]+(?:\s*-\s*[^-:]+)*):\s*\$?([\d,]+\.\d{2})",  # ✅ จับ "Item - Extra: 10.00"
        ]

    
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                if len(match.groups()) == 3:  # Quantity present
                    item_name = match.group(1).strip()
                    quantity = int(match.group(2).strip())
                    price = float(match.group(3).replace(",", "").strip())
                    total_price = quantity * price
                elif len(match.groups()) == 2:  # No quantity, default to 1
                    item_name = match.group(1).strip()
                    price = float(match.group(2).replace(",", "").strip())
                    quantity = 1
                    total_price = price
                
                parsed_data["items"].append({
                    "item_name": item_name,
                    "quantity": quantity,
                    "price": price,
                    "total_price": total_price,
                })
                break


    parsed_data["items"] = [
    item for item in parsed_data["items"] 
    if item.get("item_name", "").lower() not in ["total", "vat"]]

    return parsed_data

