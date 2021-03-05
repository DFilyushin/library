import uvicorn
from core.application import Application


if __name__ == "__main__":
    uvicorn.run(Application(), port=80)
