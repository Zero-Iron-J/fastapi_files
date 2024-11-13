#필수 프레임워크를 가져온다.
from fastapi import FastAPI
import uvicorn

# 여기서부터 파일 import
from web import market
from web import customer
from web import user
from web import html
from web import login


# app을 실행한다.
app = FastAPI()

# 이부분에 web에 작성된 router를 연결한다.
app.include_router(market.router)
app.include_router(customer.router)
app.include_router(user.router)
app.include_router(html.router)
app.include_router(login.router)

# 파일이 새로 고쳐질 때마다 서버 자동 재시작
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)