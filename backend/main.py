from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.routers import router
from app.config.db_config import async_engine
from app.core.base_model import MyBaseModel
from app.config.db_config import get_db
from app.api.v1.module_test.book.schema import BookCreate, BookUpdate

# 导入模型模块，确保它们被包含在metadata中
from app.api.v1.module_test.book.model import Book
from app.api.v1.module_test.docs.model import Document

# 创建FastAPI应用实例
app = FastAPI()

# 注册API路由
app.include_router(router)

# 允许跨域（方便前端调试）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 创建数据库表
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(MyBaseModel.metadata.create_all)


@app.get("/create_tables")
async def root():
    await create_tables()


# from app.services.milvus_service import ms
# from app.config.milvus_config import MilvusConfig


# milvus测试接口
@app.get("/milvus_test")
async def milvus_test():
    pass
    # result = ms.list_databases()
    # result = ms.list_collections("default")
    # result = ms.list_collections("milvus_demo")
    # result = ms.drop_collection("LangChainCollection", "milvus_demo")
    # result = ms.drop_database("milvus_demo")
    # result = ms.create_database("default_db")
    # result = ms.get_collection_info("demo", "default_db")
    # result = ms.create_collection(
    #     collection_name="demo",
    #     db_name="default_db",
    #     schema=schema,
    #     index_params=index_params,
    # )
    result = ms.query("demo", "default_db")
    # result = MilvusSettings.create_database()
    # result = MilvusSettings.create_collection()
    # result = MilvusSettings.drop_collection()

    return result


if __name__ == "__main__":
    import uvicorn

    # 添加reload=True参数启用自动重载功能
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    """
$env:RQ_WORKER_CLASS = 'rq.worker.SimpleWorker'
rq worker default
taskkill /pid 34396 /f
rq-dashboard
arq worker_arq.WorkerSettings
    """
