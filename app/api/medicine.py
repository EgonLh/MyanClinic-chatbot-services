from fastapi import APIRouter, Query, UploadFile, File, HTTPException
from pydantic import BaseModel
from app.services.med_service import identify_medicine

router = APIRouter(prefix="/medicine", tags=["medicine"])

# Pydantic model matching your JSON structure
class MedicineResponse(BaseModel):
    Medicine_Name: str
    Composition: str
    Uses: str
    Side_effects: str
    Image_URL: str
    Manufacturer: str
    Excellent_Review: int
    Average_Review: int
    Poor_Review: int

@router.post("/upload", response_model=MedicineResponse)
async def upload_medicine(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        result = identify_medicine(contents)

        # Map JSON keys from database to Pydantic model keys
        response = {
            "Medicine_Name": result.get("Medicine Name", "Unknown"),
            "Composition": result.get("Composition", ""),
            "Uses": result.get("Uses", ""),
            "Side_effects": result.get("Side_effects", ""),
            "Image_URL": result.get("Image URL", ""),
            "Manufacturer": result.get("Manufacturer", ""),
            "Excellent_Review": result.get("Excellent Review %", 0),
            "Average_Review": result.get("Average Review %", 0),
            "Poor_Review": result.get("Poor Review %", 0),
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

