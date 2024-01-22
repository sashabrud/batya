from fastapi import FastAPI

api = FastAPI()


@api.get("/")
def chill():
    print("Hehe")
    return "Hehe"
