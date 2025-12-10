#!/usr/bin/env python
import sys
import warnings
import os
import shutil
import zipfile
from datetime import datetime
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from engineering_team.crew import EngineeringTeam

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

output_dir = 'output'

# if os.path.exists(output_dir):
#     shutil.rmtree(output_dir)

os.makedirs(output_dir, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# requirements = """
# A simple account management system for a trading simulation platform.
# The system should allow users to create an account, deposit funds, and withdraw funds.
# The system should allow users to record that they have bought or sold shares, providing a quantity.
# The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit.
# """
requirements = """
Create a small program that lets a user manage a virtual wallet (Task: Basic Wallet Tracker).
Users can deposit money into their wallet.
Users can spend money from their wallet.
The program should show the current balance of the wallet.
"""
module_name = "wallet"
class_name = "Wallet"

class ProjectRequirements(BaseModel):
    requirements: str

def create_zip_archive():
    output_dir = "output"
    zip_path = os.path.join(output_dir, "final_delivery.zip")

    if os.path.exists(zip_path):
        os.remove(zip_path)

    # Create the zip file
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file != "final_delivery.zip":  # avoid recursion
                    full_path = os.path.join(root, file)
                    zipf.write(full_path, arcname=file)

    print(f"Created ZIP archive at: {zip_path}")
    return zip_path

def run():
    """
    Run the research crew.
    """
    inputs = {
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name
    }

    # Create and run the crew
    result = EngineeringTeam().crew().kickoff(inputs=inputs)
    create_zip_archive()

@app.post("/generate-project")
async def generate_project(req: ProjectRequirements):
    requirements = req.requirements
    inputs = {"requirements": requirements,
              "module_name": "wallet",
              "class_name": "Wallet"}

    EngineeringTeam().crew().kickoff(inputs=inputs)
    zip_path = create_zip_archive()

    return FileResponse(zip_path, filename="zip_file_final.zip") 
    # return StreamingResponse(
    #     open(zip_path, "rb"),
    #     media_type="application/zip",
    #     headers={"Content-Disposition": "attachment; filename=final_delivery.zip"}
    # )

if __name__ == "__main__":
    # run()
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)