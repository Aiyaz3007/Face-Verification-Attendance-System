import os
import cv2
import numpy as np 
import time

from facenet_pytorch import InceptionResnetV1
from retinaface import RetinaFace
import torch.nn.functional as F  

from tqdm import tqdm as loading_bar
from datetime import date
import sys

import constants
from utils import calculate_embedding,StudentDataHandler

# Load the PyTorch FaceNet model
model = InceptionResnetV1(pretrained='vggface2').eval().to(constants.device)

# Load RetinaFace detector
detector = RetinaFace(quality="normal")

# creating object for student csv handler 
student_db_handler = StudentDataHandler(json_file=constants.students_json_file,
                                        csv_file=constants.attendance_file)

students_reg_no = student_db_handler.get_all_regno()

# Load known faces and their corresponding names
known_faces = []
known_names = []


for file_path in loading_bar(student_db_handler.get_all_imagenames()):
    try:
        platform_specific_path = os.path.normpath(file_path)
        filename_with_extension = os.path.basename(platform_specific_path)
        name = os.path.splitext(os.path.basename(platform_specific_path))[0]
        print(name,filename_with_extension,platform_specific_path)
        image = cv2.imread(os.path.join(constants.known_images_folder, filename_with_extension))
        face_data = detector.predict(image)[0]

        cropped_face = image[face_data["y1"]:face_data["y2"],face_data["x1"]:face_data["x2"]]
        embedding = calculate_embedding(cropped_face,model)
        known_faces.append(embedding)
        known_names.append(name)

    except Exception as e:
        print(e)
        print(f"error occured on image: {file_path}")
        print("give some proper image") 
        sys.exit()
        


# Initialize video capture
video_capture = cv2.VideoCapture(constants.input_format)

# Initialize variables for FPS calculation
start_time = time.time()
frame_count = 0

while video_capture.isOpened():
    ret,frame = video_capture.read()
    try:
        faces = detector.predict(frame)
        for idx,face in enumerate(faces):
            if all(key in face for key in ['x1', 'y1', 'x2', 'y2']):
                x1, y1, x2, y2 = face['x1'], face['y1'], face['x2'], face['y2']
                # Extract face region from the frame
                cropped_face = frame[y1:y2, x1:x2]
                # Preprocess and extract embedding for the detected face
                detected_embedding = calculate_embedding(cropped_face,model)

                similarities = [F.cosine_similarity(detected_embedding, known_embedding).item() for known_embedding in known_faces]
                max_index = np.argmax(similarities)

                if similarities[max_index] > constants.threshold:
                    name = known_names[max_index]
                    current_student_regno = students_reg_no[max_index]
                    
                    info = student_db_handler.get_info_from_reg_no(current_student_regno)

                    print("-------------------")
                    print(info[str(date.today())])
                    print("-------------------")
                    

                    if info[str(date.today())] in ["P","A"]:
                        if info[str(date.today())] == "A":
                            student_db_handler.update_status_for_reg_no(current_student_regno,"P")
                    else:
                        student_db_handler.update_status_for_reg_no(current_student_regno,"A")
                else:
                    name = "unknown"
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)

                

    except Exception as e:
        print(e)

    # Calculate FPS
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # Display FPS on the frame
    cv2.putText(frame, f"FPS: {round(fps, 2)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("frame",frame)
    k = cv2.waitKey(1) 
    if k == 27:
        break
video_capture.release()
cv2.destroyAllWindows()