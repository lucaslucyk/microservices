from fastapi import FastAPI


app = FastAPI()


@app.get('/')
async def home():
    return {'kind': 'user-api'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        # host='0.0.0.0',
        # port=8000,
        # log_level='warning'
        # reload=True,
        # reload_dirs=[os.path.join(os.path.dirname(__file__), 'app')]
    )