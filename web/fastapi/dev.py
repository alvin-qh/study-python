if __name__ == "__main__":
    """启动测试用服务器"""
    import uvicorn

    # 启动服务器
    uvicorn.run(
        app="basic:app",
        host="0.0.0.0",
        port=5001,
        reload=True,
    )
