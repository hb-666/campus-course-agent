from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from app.config import UPLOAD_DIR
from app.models import *  # noqa: F401
from app.models.user import User
from app.database import Base, engine
from app.api import api
from starlette.middleware.cors import CORSMiddleware
from app.common.exceptions import (
    BusinessException,
    business_exception_handler,
    http_excpetion_hadler,
    validation_excpetion_hadler,
    global_excpetion_hadler,
)

Base.metadata.create_all(bind=engine)  # 自动帮我们创数据库表


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动项目开启异步的扫描任务
    yield


# Swagger UI 静态资源地址：默认的 cdn.jsdelivr.net 在国内常因 SSL 握手失败而白屏，
# 这里换成国内可访问的 CDN。如 staticfile 不可用，可改用下面这条 bootcdn：
#   https://cdn.bootcdn.net/ajax/libs/swagger-ui/5.11.0/
SWAGGER_CDN_BASE = "https://cdn.staticfile.net/swagger-ui/5.11.0"

# docs_url=None：关闭 FastAPI 默认 /docs（它硬编码引用 jsdelivr），改用下面自定义的路由
app = FastAPI(lifespan=lifespan, docs_url=None, redoc_url=None)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端源，不要直接写 ["*"]
    allow_credentials=True,  # ✅ 关键：允许前端携带 Authorization token
    allow_methods=["*"],  # 允许所有请求方法 GET POST PUT DELETE OPTIONS
    allow_headers=["*"],  # 允许所有请求头（包含Authorization）
)

app.include_router(api)

# 注册异常处理器
app.add_exception_handler(BusinessException, business_exception_handler)
app.add_exception_handler(HTTPException, http_excpetion_hadler)
app.add_exception_handler(RequestValidationError, validation_excpetion_hadler)
# 全局的异常兜底，必须放在最后注册！！
app.add_exception_handler(Exception, global_excpetion_hadler)

# 挂载静态的文件目录  http://127.0.0.1:8000/uploads/xxx.jpg
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/docs", include_in_schema=False)
def custom_swagger_ui():
    """接口文档页：静态资源走国内 CDN，避免默认 jsdelivr 在国内加载失败导致白屏。"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - Swagger UI",
        swagger_js_url=f"{SWAGGER_CDN_BASE}/swagger-ui-bundle.js",
        swagger_css_url=f"{SWAGGER_CDN_BASE}/swagger-ui.css",
    )


@app.get("/")
def root():
    return {"message": "FastAPI工程正在运行中"}
