# 使用官方Python 3.11作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖清单并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制其余所有代码
COPY . .

# 暴露Hugging Face Spaces默认的7860端口
EXPOSE 7860

# 启动FastAPI应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]