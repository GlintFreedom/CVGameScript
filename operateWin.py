import pyautogui
import pygetwindow as gw
import time
from recognizeNum import *


def capture_window(window):
    try:
        window.activate()
        time.sleep(1)  # 等待1秒确保窗口激活
        screenshot = pyautogui.screenshot(region=(window.left, window.top, window.width, window.height))
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        return frame
    except IndexError:
        print("窗口未找到")
        return None


def drag_window(window, top_left, lower_right):
    x1, y1 = top_left
    x2, y2 = lower_right
    pyautogui.moveTo(window.left + x1, window.top + y1)
    pyautogui.mouseDown()
    pyautogui.moveTo(window.left + x2, window.top + y2, duration=0.1)
    pyautogui.mouseUp()


def eliminate(digits_matrix, digit_squares, window):
    for x_len in range(1, 16):
        for y_len in range(1, 10):
            for begin_x in range(0, 16-x_len+1):
                for begin_y in range(0, 10-y_len+1):
                    sum = 0
                    for i in range(begin_x, begin_x + x_len):
                        for j in range(begin_y, begin_y + y_len):
                            sum += int(digits_matrix[i][j])
                            if sum > 10:
                                break
                        if sum > 10:
                            break
                    if sum == 10:
                        for i in range(begin_x, begin_x + x_len):
                            for j in range(begin_y, begin_y + y_len):
                                digits_matrix[i][j] = 0
                        x1, y1, x2, y2 = digit_squares[begin_x * 10 + begin_y]
                        top_left = ((x1 + x2) / 2, (y1 + y2) / 2)
                        x3, y3, x4, y4 = digit_squares[(begin_x + x_len - 1) * 10 + begin_y + y_len - 1]
                        lower_right = ((x3 + x4) / 2, (y3 + y4) / 2)
                        drag_window(window, top_left, lower_right)


if __name__ == "__main__":
    window_title = "开局托儿所"
    window = gw.getWindowsWithTitle(window_title)[0]
    screen_width, screen_height = pyautogui.size()
    times = 1
    while True:
        window_image = capture_window(window)

        if window_image is not None:
            matrix, squares = recognize_matrix(window_image)
            eliminate(matrix, squares, window)
            eliminate(matrix, squares, window)
            eliminate(matrix, squares, window)
            print(f"No.{times} game is done...")
            times += 1
            time.sleep(90)
            pyautogui.moveTo(screen_width // 2, screen_height * 2 // 3)
            pyautogui.click()
            time.sleep(5)
        else:
            print("窗口未找到。")