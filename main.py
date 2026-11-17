import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from fastapi import FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(docs_url=None)
app.openapi_version = "3.0.0"   # 新增这行，让 Swagger UI 能识别

from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.15.5/swagger-ui.css",
    )
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL")
)
model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

class GenerateRequest(BaseModel):
    topic: str
    style: str = "专业营销"

class GenerateResponse(BaseModel):
    result: str

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
def generate_text(req: GenerateRequest):
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "你是一个文案专家，请用100字以内回答。"},
                {"role": "user", "content": f"请用【{req.style}】风格，围绕“{req.topic}”写一段文案。"}
            ],
            temperature=0.7
        )
        return GenerateResponse(result=response.choices[0].message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"模型调用失败: {str(e)}")