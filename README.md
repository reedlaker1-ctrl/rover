# Camera tracker (ROS 2)

A ROS2 package designed to allow a servo-mounted camera to track an object of interest.

## Status

- [x] Package created
- [ ] fake_target node
- [ ] pan_tilt_controller node
- [ ] servo_sim node
- [ ] tracker_node (video file, then webcam)
- [ ] Launch file and params
- [ ] Hardware implementation

## Architecture


## Topics

| Topic | Type | Units / meaning | Publisher | Subscriber |
|-------|------|-----------------|-----------|------------|
| /target | ? | Normalized offset of target image center, x and y each in [-1, 1]. | fake_target/ tracker_node | pan_tilt_controller |
| /target_found | ? | ? | fake_target | pan_tilt_controller |
| /servo_cmd | ? | ? | pan_tilt_controller | servo_sim |

## Setup

Requires Ubuntu 22.04 and ROS 2 Humble.

## Usage
