from initialization import *
from our_CNN import *
import math

speed = 5
far_from_wall = 850

prev_degree = 0

def is_in_proccess_range(gps_values, first_pic_proccessed, second_pic_proccessed):
    if -13 < gps_values[0] < -10 and 1.9 < gps_values[1] < 2.1 and not second_pic_proccessed:
        second_pic_proccessed = True
        return True, first_pic_proccessed, second_pic_proccessed
    if 2.5 < gps_values[0] < 3.2 and 2.58 < gps_values[1] < 2.63 and not first_pic_proccessed:
        print('Image observed!')
        first_pic_proccessed = True
        return True, first_pic_proccessed, second_pic_proccessed
    return False, first_pic_proccessed, second_pic_proccessed

def fix_degree(degree, speed):
    dif0 = abs(degree - 0)
    dif90 = abs(degree - 90)
    dif180 = abs(degree - 180)
    dif270 = abs(degree - 270)
    dif360 = abs(degree - 360)
            
    dest = 0
    if dif90 < dif0:
        dest = 90
    if dif180 < dif90:
        dest = 180
    if dif270 < dif180:
        dest = 270
    if dif360 < dif270:
        dest = 360
                
    diff = degree - dest            
    final_speed = speed
    if diff <= 0:
        final_speed = -speed
                
    update_motor_speed([final_speed, final_speed, final_speed])
    return diff


if __name__ == "__main__":
    TIME_STEP = 32
    robot = init_robot(time_step=TIME_STEP)
    init_robot_state(in_pos=[0, 0, 0], in_omega=[0, 0, 0])
    update_motor_speed(input_omega=[0, 0, 0])

    state = 'start'
    far_from_wall_counter = 0
    go_away_wall_counter = 5
    is_proccessing = False
    first_pic_proccessed = False
    second_pic_proccessed = False
    fix_degree_counter = 0
    
    image_counter = 0
    while robot.step(TIME_STEP) != -1:
        gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()
        update_robot_state()
        in_proccess_range, first_pic_proccessed, second_pic_proccessed = is_in_proccess_range(
            gps_values, first_pic_proccessed, second_pic_proccessed)
            
        if in_proccess_range:
            image_counter += 1
            diff = 10
            while diff > 1:
                diff = fix_degree(degree, speed)
            save_image(image_counter)
            output = process_image('src_img' + str(image_counter) + '.png')
            print(output)
            if target_shape == output:
                print('Stop shape')
                update_motor_speed([0, 0, 0])
                print('Stop shape')
                break

        gps_values, compass_val, sonar_value, encoder_value, ir_value = read_sensors_values()
        front_ir_values = ir_value[0], ir_value[3]
        right_ir_values = ir_value[2], ir_value[5]
        left_ir_values = ir_value[1], ir_value[4]
        front_sonar = sonar_value[1]
        left_sonar = sonar_value[2]
        degree = get_bearing_in_degrees(compass_val)
        
        if state == 'start':
            update_motor_speed([-speed, speed, 0])

            if front_sonar < far_from_wall:
                state = 'follow_wall'

        elif state == 'follow_wall':

            far_from_wall_counter += 1
            if far_from_wall_counter == 10:
                state = 'decrease_distance'
                far_from_wall_counter = 0
            else:
                update_motor_speed([-1*speed, -1*speed, 2*speed])

            fix_degree_counter += 1
            if fix_degree_counter == 10:
                fix_degree_counter = 0
                state = 'fix_degree'

            go_away_wall_counter += 1
            if go_away_wall_counter == 10:
                go_away_wall_counter = 5
            else:
                update_motor_speed([-1*speed, -1*speed, 2*speed])

            if front_sonar == 1000:
                update_motor_speed([0, 0, 0])
                state = 'turn_right'
                prev_degree = degree

            if (ir_value[1] < 1000 or ir_value[4] < 1000):
                update_motor_speed([0, 0, 0])
                state = 'turn_left'
                prev_degree = degree

        elif state == 'turn_right':
            update_motor_speed([-speed, 0, speed*2])

            if abs(prev_degree - degree) > 90:
                state = 'increase_distance'

        elif state == 'decrease_distance':
            update_motor_speed(input_omega=[-1*speed, speed, 0])
            if front_sonar < far_from_wall or front_sonar == 1000:
                state = 'follow_wall'

        elif state == 'turn_left':
            update_motor_speed([-speed, -speed, -speed])
            if abs(prev_degree - degree) > 90:
                state = 'increase_distance'

        elif state == 'increase_distance':
            update_motor_speed([1*speed, -2*speed, speed])

            if front_sonar > far_from_wall:
                state = 'follow_wall'

        elif state == 'fix_degree':
            diff = fix_degree(degree, speed)
            
            if diff < 1:
                state = 'follow_wall'
