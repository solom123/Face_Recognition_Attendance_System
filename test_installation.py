# import dlib
# import face_recognition
# import numpy as np

# print("dlib version:", dlib.__version__)

# print("Dlib CUDA available:", dlib.DLIB_USE_CUDA) # type: ignore
# print("Dlib CUDA devices:", dlib.cuda.get_num_devices() if dlib.DLIB_USE_CUDA else "N/A") # type: ignore

# print("face_recognition version:", face_recognition.__version__)

# img = np.zeros((128,128,3), dtype=np.uint8)

# print("Face encodings:", face_recognition.face_encodings(img))

# import face_recognition
# print(face_recognition.__version__)
# print(face_recognition.__file__)

# -------------------------------------------------------------------------------------

# from PIL import Image
# import numpy as np

# img_path = "Images/Anand_Photo_1.jpg"
# try:
#     pil_img = Image.open(img_path).convert('RGB')
#     np_img = np.array(pil_img)
#     print("shape:", np_img.shape)
#     print("dtype:", np_img.dtype)
# except Exception as e:
#     print("Error:", e)


import face_recognition

image_path = "Images/1 (1).jpg"  # Change to any image in your folder

image = face_recognition.load_image_file(image_path)

# Find face locations
face_locations = face_recognition.face_locations(image)
print("Detected face locations:", face_locations)

# Get face encodings
face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)
print("Number of face encodings found:", len(face_encodings))


# -------------------------------------------------------------------------------------
