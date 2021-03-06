#coding=utf-8
import numpy as np
import datetime 

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist 
from tf.transformations import euler_from_quaternion, quaternion_from_euler

# def get_rotation (msg):
#     global roll, pitch, yaw
#     orientation_q = msg.pose.pose.orientation
#     orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
#     (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
#     print (yaw)

# rospy.init_node('my_quaternion_to_euler')

# sub = rospy.Subscriber ('/odom', Odometry, get_rotation)

# r = rospy.Rate(1)
# while not rospy.is_shutdown():
#     r.sleep()


# from scipy.optimize import brute 
# import itertools 

# def f(x): 
#     return (481.79/(5+x[0]))+(412.04/(4+x[1]))+(365.54/(3+x[2])) 

# ranges = (slice(0, 9, 1),) * 3 

# print slice(0, 9, 1)

# result = brute(f, ranges, disp=True, finish=None) 
# print(result) 

#结果转化为控制量
def result_to_control(result):
    #创建控制量(总共六组)
    control = []
    temp = np.array([[0,0],[0,0],[0,0]])

    #创建循环进行数值转换
    for num in range(6):
        if result[num] == 0: #直行
            temp[0,0]= 1 
            temp[0,1]= 0

            #转化成list并赋值
            control.append(temp.tolist()[0])

            print("0")
        if result[num] == 1: #左转一圈
            #先转动
            temp[0,0]= 0 
            temp[0,1]= 1

            #再直行
            temp[1,0]= 1 
            temp[1,1]= 0

            # #转化成list并赋值
            # control.append(temp.tolist()[0:2])
            control = control +temp.tolist()[0:2]

            print("1")
        if result[num] == 2: #左转两圈
            #先转动
            temp[0,0]= 0 
            temp[0,1]= 1

            #再转动
            temp[1,0]= 0 
            temp[1,1]= 1

            #再直行
            temp[2,0]= 1 
            temp[2,1]= 0

            #转化成list并赋值
            #control.append(temp.tolist()[0:3])
            control = control +temp.tolist()[0:3] #直接加就行

            print("2")

        if result[num] == 3: #右转一圈
            #先转动
            temp[0,0]= 0 
            temp[0,1]= -1

            #再直行
            temp[1,0]= 1 
            temp[1,1]= 0

            #转化成list并赋值
            control.append(temp.tolist()[0:2])

            print("3")

        if result[num] == 4: #左转两圈
            #先转动
            temp[0,0]= 0 
            temp[0,1]= -1

            #再转动
            temp[1,0]= 0 
            temp[1,1]= -1

            #再直行
            temp[2,0]= 1 
            temp[2,1]= 0

            #转化成list并赋值
            control.append(temp.tolist()[0:3])

            print("4")

        #数值重置
        temp = np.array([[0,0],[0,0],[0,0]])
    
    return control


#将控制量发布出去
def control_publish(control):
    #初始化node
    rospy.init_node('mpc_brute', anonymous=True)

    #初始化publisher 
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10) # topic和消息类型需要和肖岸星商量确定一下 
        
    #初始化twist
    twist = Twist()

    #将所有数据发送出去
    for num in range(len(control)):
        # 给twist赋值（已经没有了四元素的含义了）
        twist.linear.x = np.asarray(control)[num,0] #线速度
        twist.linear.y = 0.0
        twist.linear.z = 0.0

        twist.angular.x = 0.0 
        twist.angular.y = 0.0
        twist.angular.z = np.asarray(control)[num,1] #角速度

        #发送twist
        pub.publish(twist) #将数据发送出去

        print("twist",twist) 



# result= [1,2,1,1,1,1]

# xx = result_to_control(result)

# control_publish(xx)

# print(xx)

# print(np.asarray(xx))

# print(np.asarray(xx)[0,1])

# print(len(xx))

# print(len(np.asarray(xx)))

# print(xx[1])

for i in range(5):
    print("ok")
