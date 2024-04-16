from fastapi import FastAPI, Request, HTTPException
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
