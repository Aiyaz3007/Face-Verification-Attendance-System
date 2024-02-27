

# Face Verification Attendance System

This is a Face Verification Attendance System utilizing RetinaFace and InceptionResnetV1 for face recognition.

## Installation

### Python Version
This project requires Python 3.7.0. Please ensure you have Python 3.7.0 installed.

### Running requirements.txt
Before running the system, ensure you have installed the required dependencies by executing:


## Configuration Changes

### Constants.py
In the `constants.py` file, you can find the following configurations:

```python
# Known face database
database_path = "./known_images"
db_json_file = database_path + "/students_db.json"

# Inference
"""
0 - webcam
'video.mp4' - input video
"""
input_format = "sriram.mp4"
# input_format = 0

students_json_file = "./student_db/students_info.json"
attendance_file = "./student_db/attendance.csv"
known_images_folder = "./student_db/images"  # Path to the folder of known images

threshold = 0.7

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

red = (255,0,0)
green = (0,255,0)
font = cv2.FONT_HERSHEY_SIMPLEX

```
## Running the System

```
python main.py
