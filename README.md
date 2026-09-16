# ros_hand_gesture_robot

Hệ thống ROS điều khiển robot mô phỏng bằng nhận diện cử chỉ tay từ webcam.

## Tổng quan

Repository gồm 3 package ROS:

- **my_cam**: đọc ảnh từ camera và publish lên topic `image_raw`.
- **ros_hand_gesture_recognition**: nhận ảnh, nhận diện cử chỉ tay bằng MediaPipe + TensorFlow Lite, publish nhãn cử chỉ.
- **ros_mobile_robot**: mô phỏng robot 4 bánh vi sai trong Gazebo/RViz và nhận lệnh `cmd_vel`.

Luồng dữ liệu chính:

`Webcam -> /image_raw -> nhận diện cử chỉ -> chuyển cử chỉ thành Twist -> /robot_diff_drive_controller/cmd_vel -> robot di chuyển`

## Cấu trúc thư mục

```text
.
├── my_cam/
│   ├── launch/my_cam.launch
│   └── src/
│       ├── image_publisher_launch.py
│       ├── image_publisher.py
│       └── image_subscriber.py
├── ros_hand_gesture_recognition/
│   ├── launch/
│   │   ├── hand_sign.launch
│   │   └── sign_control.launch
│   ├── src/
│   │   ├── hand_sign_recognition.py
│   │   ├── sign_to_controller.py
│   │   ├── gesture_recognition.py
│   │   └── model/
│   │       └── keypoint_classifier/
│   │           ├── keypoint_classifier.tflite
│   │           └── keypoint_classifier_label.csv
│   └── README.md
└── ros_mobile_robot/
    ├── launch/mobile_robot.launch
    ├── config/diffdrive.yaml
    └── urdf/mobile_robot.urdf.xacro
```

## Điều kiện cần

- ROS 1 (catkin workspace)
- Python 3
- Các package ROS phụ thuộc (theo `package.xml`):
  - `rospy`, `sensor_msgs`, `std_msgs`
- Thư viện Python dùng trong nhận diện cử chỉ:
  - `mediapipe`
  - `opencv-python`
  - `tensorflow` (dùng model TFLite)
  - `numpy`

## Cài đặt

1. Clone repository vào thư mục `src` của catkin workspace:

```bash
git clone https://github.com/jungle-02/ros_hand_gesture_robot.git
```

2. Build workspace:

```bash
cd ~/catkin_ws
catkin_make
# hoặc catkin build
```

3. Source môi trường:

```bash
source ~/catkin_ws/devel/setup.bash
```

## Cách chạy

### 1) Chạy mô phỏng robot

```bash
roslaunch ros_mobile_robot mobile_robot.launch
```

### 2) Chạy pipeline camera + nhận diện cử chỉ + điều khiển robot

```bash
roslaunch ros_hand_gesture_recognition sign_control.launch
```

`sign_control.launch` tự include:

- `my_cam/launch/my_cam.launch`
- `ros_hand_gesture_recognition/launch/hand_sign.launch`

## Mapping cử chỉ -> điều khiển

Node `sign_to_controller.py` chuyển nhãn cử chỉ thành vận tốc:

- `Forward`: tăng `linear.x`
- `Backward`: giảm `linear.x`
- `Turn Right`: giảm `angular.z`
- `Turn Left`: tăng `angular.z`
- `Stop` / `NONE`: đặt `linear.x = 0`, `angular.z = 0`

## Topic chính

- Camera output: `/image_raw`
- Gesture output: `/gesture/hand_sign`
- Robot velocity command: `/robot_diff_drive_controller/cmd_vel`

## Huấn luyện lại model cử chỉ

Repository đã có notebook và dữ liệu mẫu trong:

- `ros_hand_gesture_recognition/src/notebooks/keypoint_classification_EN.ipynb`
- `ros_hand_gesture_recognition/src/model/keypoint_classifier/keypoint.csv`
- `ros_hand_gesture_recognition/src/model/keypoint_classifier/keypoint_classifier_label.csv`

Hướng dẫn chi tiết tham khảo thêm tại:

- `ros_hand_gesture_recognition/README.md`

## Giấy phép

- `ros_hand_gesture_recognition` chứa file `LICENSE`.
- Các package còn lại đang để license dạng placeholder trong `package.xml`.
