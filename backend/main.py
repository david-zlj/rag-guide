# TODO 接口文档UI
import uvicorn
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
from app.config.base_model import MyBaseModel
from app.config.db_config import get_db
from app.api.v1.module_test.book.schema import BookCreate, BookUpdate

# 导入模型类，否则数据库表不会被创建
from app.api.v1.module_test.book.model import Book
from app.api.v1.module_rag.docs.model import Document

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


@app.post("/create_tables", summary="创建数据库表")
async def create_tables():
    """
    创建数据库表
    条件：导入模型类
    """
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(MyBaseModel.metadata.create_all)
        return {"message": "数据库表创建成功"}
    except Exception as e:
        return {"error": str(e)}


from app.services.reranker.reranker_factory import RerankerFactory


# reranker测试接口
@app.get("/reranker_test")
async def reranker_test():
    reranker = RerankerFactory.get_reranker()
    result = await reranker.arerank_documents(
        query="你好",
        documents=[
            "你好，我是文档1",
            "你好，我是文档2",
            "你好，我是文档3",
        ],
        top_k=2,
    )
    return result


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

    """
$env:RQ_WORKER_CLASS = 'rq.worker.SimpleWorker'
rq worker default
taskkill /pid 34396 /f
rq-dashboard
arq arq_worker.WorkerSettings
    """
