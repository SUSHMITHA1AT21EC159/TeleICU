import cv2
import os
import requests
import time

# Function to download file from Google Drive
def download_file_from_google_drive(file_id, destination):
    URL = "https://drive.google.com/uc?id=" + file_id
    session = requests.Session()
    response = session.get(URL, stream=True)
    token = None

    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
            break

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)

# Function to extract frames from video and measure performance
def extract_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    count = 0
    total_time = 0

    while cap.isOpened():
        start_time = time.time()  # Start time for current frame
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(os.path.join(output_folder, f'frame_{count}.jpg'), frame)
        count += 1
        end_time = time.time()  # End time for current frame
        frame_time = end_time - start_time
        total_time += frame_time
        print(f"Frame {count}: Time taken = {frame_time:.4f} seconds")

    cap.release()

    # Calculate and print FPS
    fps = count / total_time
    print(f"FPS: {fps:.2f}")

# Google Drive shared link for the video
google_drive_url = 'https://drive.google.com/file/d/1DDrgiqwKG-wDMx-Dbi19yRz75i-eg-sy/view?usp=sharing'

# Extract file ID from the Google Drive URL
file_id = google_drive_url.split('/')[-2]

# Local path to save the downloaded video
video_path = 'sample_video.mp4'

# Output folder for extracted frames
output_folder = 'extracted_frames'

# Download video from Google Drive
download_file_from_google_drive(file_id, video_path)

# Extract frames from the downloaded video and measure performance
extract_frames(video_path, output_folder)
