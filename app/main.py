import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


from app.api.v1 import api_router
from app.core import settings

# *******************************************************************************
# FASTAPI APP SETTINGS
# *******************************************************************************

app = FastAPI(
    title="Awesome FastAPI Boilerplate",
    description="An starter boilerplate for getting familiar with FastAPY",
    version="1.0.0",
    terms_of_service="http://project_name.com/terms/",
    contact={
        "name": "Samuel Valdes Gutierrez",
        "url": "https://github.com/BigSamu",
        "email": "valdesgutierrez@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://github.com/BigSamu/Awesome-FastAPI-Boilerplate/blob/main/LICENSE.md",
    }
)

# *******************************************************************************
# DATABASE INITIALIZATION
# *******************************************************************************

from app.database import init_database

# Initialise the database
init_database()


# *******************************************************************************
# CORS SETTINGS
# *******************************************************************************

origins = [
    "localhost:3000",
    "http://localhost",
    "http://localhost:3000",
    "https://localhost",
    "https://localhost:3000",
    "http://127.0.0.1:3000",
    "https://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# *******************************************************************************
# ROUTE SETTINGS
# *******************************************************************************

app.include_router(api_router, prefix=settings.API_V1_STR)

# *******************************************************************************
# STATIC FOLDER SETTINGS
# *******************************************************************************

#  Make images folder statically available
app.mount("/images", StaticFiles(directory="app/static/images"), name="images")


# *******************************************************************************
# RUN SETTINGS
# *******************************************************************************

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
