import math
import time

def get_sin_value(t):
    # sin 函数的值范围是 [-1, 1]
    # 将其映射到 [10, 40] 的范围
    amplitude = (40 - 10) / 2  # 振幅 = (最大值 - 最小值) / 2 = 15
    offset = (40 + 10) / 2     # 偏移 = (最大值 + 最小值) / 2 = 25
    
    # 使用 sin 函数计算当前值
    value = amplitude * math.sin(t) + offset
    return value

# 测试代码
if __name__ == "__main__":
    # 通过改变这个数值可以控制循环的速度
    SPEED = 0.1  
    
    while True:
        # 使用当前时间作为参数，这样可以随时间自动变化
        current_time = time.time()
        value = get_sin_value(current_time * SPEED)
        print(f"当前值: {value:.2f}")
        time.sleep(0.1)  # 每0.1秒更新一次 