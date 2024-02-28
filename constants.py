import torch
import cv2

# --------------------- inputs ----------------------

# known face  
database_path = "./known_images"
db_json_file = database_path + "/students.json"

#inference
"""
0 - webcam
'video.mp4' - input video
"""
# input_format = "class.mp4"
input_format = 0


students_json_file = "./student_db/students_info.json"
attendance_file = "./student_db/attendance.csv"
known_images_folder = "./student_db/images"  # Path to the folder of known images


threshold = 0.7

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


red = (255,0,0)
green = (0,255,0)
font = cv2.FONT_HERSHEY_SIMPLEX