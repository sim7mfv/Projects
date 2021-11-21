from fastapi import FastAPI, Response, HTTPException, status, Query, Body
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import StreamingResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CountryIn(BaseModel):
    names: List[str]

class CountryOut(BaseModel):
    iso_code: str
    shape: Optional[str] = None


with open("countries.geojson") as countries_file:
    data = json.load(countries_file)

@app.get("/")
def homepage():
    return {"home" : "page"}
#iso_code: Param: 1+ country names, option param "details" - if true returns geometries // Return: ISO3 country codes
@app.post("/iso_code", response_model=List[CountryOut])
def iso_code(countries: CountryIn, details: Optional[bool] = None):
    result = []
    for country in countries.names:
        for each in data["features"]:
            if country == each["properties"]["name"]:
                if details == True:
                    result.append(CountryOut(iso_code=each["id"], shape=each["geometry"]["type"]))
                else:
                    result.append(CountryOut(iso_code=each["id"]))
    return result


#all_geometreis: get all contents of file in one go
@app.get("/all_geometries", response_class=StreamingResponse)
def get_all():
    def get_file():
        with open("countries.geojson", mode="rb") as temp_file:
            yield from temp_file
    return StreamingResponse(get_file(), media_type="text/csv")