# from utils import StudentDataHandler
# import constants

# # creating object for student csv handler 
# student_db_handler = StudentDataHandler(json_file=constants.students_json_file,
#                                         csv_file=constants.attendance_file)
# # print(student_db_handler.create_csv_file())
# # print(student_db_handler.get_all_regno())


# for file_name in (student_db_handler.get_all_imagenames()):
#     print(file_name)

import os

# Define the file path
file_path = ".\images\sriram.jpg"

# Convert the file path to the platform-specific path
platform_specific_path = os.path.normpath(file_path)

# Extract the filename without extension
filename = os.path.splitext(os.path.basename(platform_specific_path))[0]

print(filename)
