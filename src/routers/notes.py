from fastapi import APIRouter, UploadFile, File, HTTPException, Form
import cloudinary.uploader
import cloudinary.api
from typing import List
import uuid
from pydantic import BaseModel
from ..config.mongodb_config import get_collection as mongo_get_collection
from ..utils.process import process_files
from ..config.milvus_config import get_collection as milvus_get_collection

router = APIRouter()

mongo_notes = mongo_get_collection("javafest", "notes")
milvus_notes = milvus_get_collection("notes")

@router.post("/notes")
async def upload_note(files: List[UploadFile] = File(...),
                      email: str = Form(...),
                      title: str = Form(...),
                      description: str = Form(...)):
    try:
   
        allowed_file_types = {"image/jpeg", "image/png", "image/jpg", "image/gif"}

        max_size = 5 * 1024 * 1024  # 5MB
        for file in files:
            if file.content_type not in allowed_file_types:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' is not a valid image (allowed: JPEG, PNG, GIF)"
                )
            if file.size > max_size:
                raise HTTPException(
                    status_code=400,
                    detail=f"File '{file.filename}' exceeds 5MB limit"
                )
        
        folder_id = f'notes/{email}/{uuid.uuid4()}'  
        files_url = []
        public_ids = []
        for file in files:
            # Upload each file to Cloudinary
            response = cloudinary.uploader.upload(
                file.file,
                folder=folder_id,
            )
            files_url.append(response.get("secure_url"))
            public_ids.append(response.get("public_id"))
            
            response = process_files(response.get("secure_url"))
            vector_metadata = {
                "vector": response.get("vector"),
                "folder_id": folder_id,
                "email": email,
                "title": title,
                "text": response.get("text")
            }
            milvus_notes.insert([vector_metadata])


        file_metadata = {
            "email": email,
            "title": title,
            "description": description,
            "folder_id": folder_id,
            "public_ids": public_ids,
            "urls": files_url,
        }

        # Save metadata to MongoDB
        mongo_notes.insert_one(file_metadata)
        return {"success": True, "folder_id": folder_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Define a Pydantic model for the request body
class DeleteNotesRequest(BaseModel):
    folder_id: str


@router.delete("/notes")
async def delete_notes(request: DeleteNotesRequest):
    folder_id = request.folder_id
    if not folder_id:
        raise HTTPException(status_code=400, detail="folder_id is required")
    
    try:
        public_ids = mongo_notes.find_one({"folder_id": folder_id})["public_ids"]
        print(public_ids)
        for public_id in public_ids:
            cloudinary.uploader.destroy(public_id)
        # Delete the folder
        cloudinary.api.delete_folder(folder_id)
        # Delete related notes from the database
        mongo_notes.delete_one({"folder_id": folder_id})
        # Delete related notes from Milvus
        filter_expr = f'folder_id == "{folder_id}"'
        milvus_notes.delete(expr=filter_expr)
        return {"success": True,"message": "Folder and its contents deleted successfully"}
     
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")