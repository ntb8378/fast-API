import uuid
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status

app = FastAPI()

# Cấu hình hằng số
UPLOAD_FOLDER = Path("storage/documents")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".ppt", ".pptx"}
ALLOWED_DOC_TYPES = {"lecture", "assignment", "reference"}

# Tự động tạo thư mục với parents=True, exist_ok=True để tránh crash
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

@app.post("/documents")
async def upload_document(
    title: str = Form(...),
    course_code: str = Form(...),
    document_type: str = Form(...),
    description: str = Form(""),
    document: UploadFile = File(...),
):
    # 1. Kiểm tra tiêu đề (chặn rỗng/khoảng trắng)
    title = title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Tên tài liệu không được để trống"
        )

    # 2. Chuẩn hóa mã môn học thành chữ hoa
    course_code = course_code.strip().upper()

    # 3. Kiểm tra loại tài liệu
    if document_type not in ALLOWED_DOC_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Loại tài liệu không hợp lệ. Chỉ chấp nhận: {', '.join(ALLOWED_DOC_TYPES)}"
        )

    # 4. Lấy phần mở rộng file (suffix) và chuyển thành chữ thường
    # Path(filename).suffix sẽ lấy chính xác đuôi cuối cùng (vd: ".exe" từ "baitap.pdf.exe")
    # Gắn fallback an toàn nếu document.filename trả về None
    original_filename = document.filename or "unknown_file"
    extension = Path(original_filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Định dạng file không được phép"
        )

    # 5. Đọc nội dung file để kiểm tra kích thước và file rỗng
    content = await document.read()
    file_size = len(content)

    if file_size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="File tải lên không được rỗng"
        )

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, 
            detail="Kích thước file không được vượt quá 10 MB"
        )

    # 6. Đổi tên file bằng UUID để đảm bảo duy nhất, tránh ghi đè và tránh Path Traversal
    unique_filename = f"{uuid.uuid4()}{extension}"
    file_path = UPLOAD_FOLDER / unique_filename

    # 7. Ghi file xuống ổ đĩa
    with open(file_path, "wb") as output_file:
        output_file.write(content)

    # Trả về kết quả
    return {
        "success": True,
        "message": "Upload tài liệu thành công",
        "data": {
            "title": title,
            "course_code": course_code,
            "document_type": document_type,
            "description": description.strip(),
            "original_filename": original_filename,  # Lưu lại tên gốc
            "saved_filename": unique_filename,       # Tên file an toàn lưu trên server
            "file_path": str(file_path),             # Đường dẫn
        },
    }