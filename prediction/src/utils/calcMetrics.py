import math
def calculate_density(frame_data):
    return len(frame_data)


def calculate_avg_speed(prev_frame, curr_frame, time_delta=1.0):
    if not curr_frame or not prev_frame:
        return 0.0

    prev_positions = {}
    for detection in prev_frame:
        for obj_id, bbox in detection.items():
            prev_positions[obj_id] = bbox

    speeds = []
    for detection in curr_frame:
        for obj_id, bbox in detection.items():
            if obj_id in prev_positions:
                x1_prev, y1_prev, x2_prev, y2_prev = prev_positions[obj_id]
                x1_curr, y1_curr, x2_curr, y2_curr = bbox

                prev_center = ((x1_prev + x2_prev) / 2, (y1_prev + y2_prev) / 2)
                curr_center = ((x1_curr + x2_curr) / 2, (y1_curr + y2_curr) / 2)

                distance = math.hypot(curr_center[0] - prev_center[0],
                                      curr_center[1] - prev_center[1])
                speeds.append(distance / time_delta)

    return sum(speeds) / len(speeds) if speeds else 0.0


def process_vid_data(data, time_delta=1.0):
    vid_id = data.get("vid_id")
    frames = data.get("detections", [])

    output = []

    prev_frame = []
    for frame in frames:
        frame_density = calculate_density(frame)
        frame_avg_speed = calculate_avg_speed(prev_frame, frame, time_delta)
        frame_flow = frame_avg_speed * frame_density

        output.append({
            "avg_speed": frame_avg_speed,
            "density": frame_density,
            "flow": frame_flow
        })

        prev_frame = frame

    return vid_id, output



