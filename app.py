import requests
from flask import Flask ,request,jsonify

app=Flask(__name__)

inventory=[]

def fetch_product(barcode):
    url=f"https://openfoodfacts.net{barcode}.json"
    try:
        headers={"User-Agent":"RetailInventorySystem"}
        response=requests.get(url,headers=headers, timeout=5)
        if response.status_code==200:
            data=response.json()
            if data.get('status')==1:
                product=data.get('product',{})
                # clean categories array
                raw_categories=product.get("categories","General")
                category_list=[c.strip() for c in raw_categories.split(",") if c]
                main_category=(category_list[0]if category_list else "General")
                return{"name":product.get("product_name","Unknown Product"),"category":main_category}
    except Exception:
        pass
    return None

@app.route("/inventory",methods=["POST"])
def create_item():
    data=request.get_json()
    barcode=data.get("barcode")
    if not barcode:
        return jsonify({"error":"Barcode field is required"}),400
    if any(item["barcode"]==barcode for item in inventory):
        return jsonify({"error":f"Product {barcode}already exists"}),400
    # integrate fetched data from openfoodfacts
    api_data=fetch_product(barcode)
    name=data.get("name") or (api_data.get("name")if api_data else "Unknown Product")
    category=data.get("category") or (api_data.get("category")if api_data else "General")
    new_item={"barcode":str(barcode),"name":name, "category":category, "quantity":int(data.get("quantity",0)),"price":float(data.get("price",0))}
    inventory.append(new_item)
    return jsonify(new_item),201

@app.route("/inventory",methods=["GET"])
def get_all_items():
    return jsonify(inventory),200

@app.route("/inventory/<string:barcode>",methods=["GET"])
def get_item(barcode):
    for item in inventory:
        if item["barcode"]==barcode:
            return jsonify(item),200
    return jsonify({"error":"Product not found"}),404

@app.route("/inventory/<string:barcode>",methods=["PUT"])
def update_item(barcode):
    data=request.get_json()
    for item in inventory:
        if item["barcode"]==barcode:
            item["name"]=data.get("name",item["name"])
            item['category']=data.get("category",item['category'])
            item["quantity"]=data.get("quantity",item["quantity"])
            item["price"]=data.get("price",item["price"])
            return jsonify(item),200
    return jsonify({"error":"Product not found"}),404

@app.route("/inventory/<string:barcode>",methods=["DELETE"])
def delete_item(barcode):
    global inventory
    item=next((item for item in inventory if item["barcode"]==barcode),None)
    if not item:
        return jsonify({"error":"Product not found"}),404
    inventory=[item for item in inventory if item["barcode"]!=barcode]
    return jsonify({"message":f"Product {barcode} was removed successfully"}),204

    
if __name__ == "__main__":
    app.run(debug=True)
