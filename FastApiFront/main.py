from typing import List

from fastapi import FastAPI, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from pathlib import Path

from starlette.responses import JSONResponse

app = FastAPI()

# 定义 HTML 页面文件路径
html_file_path = Path("static/index1.html")
html_file_path2 = Path("static/index2.html")

product_details = {
    1: {
        "id": 1,
        "name": "商品1",
        "description": "这是商品1的详细描述。",
        "price": 100.0,
        "published_date": "2023-01-04"
    },
    2: {
        "id": 2,
        "name": "商品2",
        "description": "这是商品2的详细描述。",
        "price": 100.0,
        "published_date": "2023-01-04"
    },
    3: {
        "id": 3,
        "name": "商品3",
        "description": "这是商品3的详细描述。",
        "price": 100.0,
        "published_date": "2023-01-04"
    },
    4: {
        "id": 4,
        "name": "商品4",
        "description": "这是商品4的详细描述。",
        "price": 100.0,
        "published_date": "2023-01-04"
    }
    # 可以添加更多商品数据
}

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

# 模拟商品数据
products_detail_data = {
    1: {"detail_name": "Product 1", "produced_at": "2024-04-25", "price": 100, "description": "This is product 1"},
    2: {"detail_name": "Product 2", "produced_at": "2024-04-25", "price": 150, "description": "This is product 2"},
    3: {"detail_name": "Product 3", "produced_at": "2024-04-25", "price": 200, "description": "This is product 3"},
    4: {"detail_name": "Product 4", "produced_at": "2024-04-25", "price": 120, "description": "This is product 4"},
    5: {"detail_name": "Product 5", "produced_at": "2024-04-25", "price": 180, "description": "This is product 5"},
    6: {"detail_name": "Product 6", "produced_at": "2024-04-25", "price": 220, "description": "This is product 6"},
    7: {"detail_name": "Product 7", "produced_at": "2024-04-25", "price": 250, "description": "This is product 7"},
    8: {"detail_name": "Product 8", "produced_at": "2024-04-25", "price": 300, "description": "This is product 8"},
    9: {"detail_name": "Product 9", "produced_at": "2024-04-25", "price": 350, "description": "This is product 9"},
    10: {"detail_name": "Product 10", "produced_at": "2024-04-25", "price": 400, "description": "This is product 10"},
    11: {"detail_name": "Product 11", "produced_at": "2024-04-25", "price": 450, "description": "This is product 11"},
    12: {"detail_name": "Product 12", "produced_at": "2024-04-25", "price": 500, "description": "This is product 12"}


}


class ProductDetail(BaseModel):
    detail_name: str
    produced_at: str
    price: float
    description: str


@app.get("/product/{product_id}/detail")
async def get_product_detail(product_id: int = Path(..., title="The ID of the product you want to get")):
    if product_id < 1 or product_id > len(products_data):
        raise HTTPException(status_code=404, detail="Product ID not found")

    product_info = products_detail_data[product_id]
    product_detail = ProductDetail(
        detail_name=product_info["detail_name"],
        produced_at=product_info["produced_at"],
        price=product_info["price"],
        description=product_info["description"]
    )

    return jsonable_encoder(product_detail)


# 模拟商品数据
products_data = {
    1: {"name": "Product 1", "created_at": "2024-04-25"},
    2: {"name": "Product 2", "created_at": "2024-04-25"},
    3: {"name": "Product 3", "created_at": "2024-04-25"},
    4: {"name": "Product 4", "created_at": "2024-04-25"},
    5: {"name": "Product 5", "created_at": "2024-04-25"},
    6: {"name": "Product 6", "created_at": "2024-04-25"},
    7: {"name": "Product 7", "created_at": "2024-04-25"},
    8: {"name": "Product 8", "created_at": "2024-04-25"},
    9: {"name": "Product 9", "created_at": "2024-04-25"},
    10: {"name": "Product 10", "created_at": "2024-04-25"},
    11: {"name": "Product 11", "created_at": "2024-04-25"},
    12: {"name": "Product 12", "created_at": "2024-04-25"},

}


class Product(BaseModel):
    name: str
    created_at: str
    detail_url: str


class ProductList(BaseModel):
    products: List[Product]
    current_page: int
    next_page_url: str


@app.get("/get_products/")
async def get_products(product_id: int):
    print('product_id::',product_id)
    if product_id < 1 or product_id > len(products_data):
        raise HTTPException(status_code=404, detail="Product ID not found")

    products = []
    start_index = (product_id - 1) * 5 + 1
    end_index = min(start_index + 5, len(products_data) + 1)
    print('start_index:: ',start_index,'end_index::',end_index)
    for i in range(start_index, end_index):
        product_info = products_data[i]
        product_detail_url = f"/product/{i}/detail"
        product = Product(
            name=product_info["name"],
            created_at=product_info["created_at"],
            detail_url=product_detail_url
        )
        products.append(product)
    print('products ::',products)
    current_page = product_id
    next_page_url = f"/get_products/?product_id={product_id + 1}" if product_id < len(products_data) / 5 else ''

    return jsonable_encoder(ProductList(products=products, current_page=current_page, next_page_url=next_page_url))


@app.get("/products", response_class=HTMLResponse)
async def get_product_list_page(request: Request):
    # 获取请求参数中的页码
    page = request.query_params.get('page', '1')

    # 检查请求中的页码
    if page == '1':
        # 返回存储的静态 HTML 页面内容
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    elif page=='2':
        with open(html_file_path2, "r", encoding="utf-8") as file:
            html_content = file.read()
        return HTMLResponse(content=html_content)
    else:

        return HTMLResponse(content="<h1>Page not found</h1>", status_code=404)
#/detail/4
@app.get("/detail/{item_id}")
async def get_product_detail(item_id: int):
    # 根据请求中的 item_id 参数获取商品详情
    product_detail = product_details.get(item_id)

    # 如果商品详情存在，返回 JSON 响应
    if product_detail:
        return JSONResponse(content=product_detail)
    else:
        # 如果没有找到对应的商品详情，返回 404 错误响应
        raise HTTPException(status_code=404, detail="Product not found")




if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
