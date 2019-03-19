import sys

sys.path.append('Windows')

import Leap
import ctypes
import time
import math

win32 = ctypes.windll.user32


def mouse_control(self, xx, yy):
    self.MOUSE_X = xx
    self.MOUSE_Y = yy
    if self.MOUSE_X > self.SCREEN_X:
        self.MOUSE_X = self.SCREEN_X
    if self.MOUSE_Y > self.SCREEN_Y:
        self.MOUSE_Y = self.SCREEN_Y
    if self.MOUSE_X < 0.0:
        self.MOUSE_X = 0.0
    if self.MOUSE_Y < 0.0:
        self.MOUSE_Y = 0.0


def point_move_mouse(self, normalizedPosition):
    xx = normalizedPosition.x * self.SCREEN_X
    yy = self.SCREEN_Y - normalizedPosition.y * self.SCREEN_Y
    mouse_control(self, xx, yy)
    win32.SetCursorPos(int(self.MOUSE_X), int(self.MOUSE_Y))


def point_move_scroll(self, finger):
    # スクロール
    scroll_y = finger.tip_velocity[1]
    scroll_y = scroll_y + math.copysign(500, scroll_y)
    scroll_y = scroll_y / 100
    scroll_y = scroll_y * 83
    scroll_y = scroll_y / 8
    # scroll_y = scroll_y * -1
    win32.mouse_event(0x0800, 0, 0, int(scroll_y), 0)


class Finger_Mouse(Leap.Listener):
    screen = None
    MOUSE_X = 0
    MOUSE_Y = 0
    SCREEN_X = win32.GetSystemMetrics(0) - 1
    SCREEN_Y = win32.GetSystemMetrics(1) - 1

    def on_init(self, controller):
        print("FingerControl Initialized")

    def on_connect(self, controller):
        # Enable gestures
        # controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        # controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        # controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

        controller.config.set("Gesture.KeyTap.MinDownVelocity", 1.0)
        controller.config.set("Gesture.KeyTap.HistorySeconds", .1)
        controller.config.set("Gesture.KeyTap.MinDistance", .1)
        controller.config.save()
        print("FingerControl Connected")

    def on_disconnect(self, controller):
        print("FingerControl Disconnected")

    def on_exit(self, controller):
        print("FingerControl Exited")

    def on_frame(self, controller):
        frame = controller.frame()
        hand = frame.hands.frontmost
        finger = frame.fingers.frontmost

        stabilizedPosition = finger.stabilized_tip_position
        interactionBox = frame.interaction_box
        normalizedPosition = interactionBox.normalize_point(stabilizedPosition)

        # 指の数判定
        finger_count = len(frame.fingers.extended())
        gesture = frame.gestures()[0]
        if finger.touch_zone > 0:
            if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                if finger_count == 1:
                    if gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                        win32.mouse_event(0x02, 0, 0, 0, 0)
                        win32.mouse_event(0x04, 0, 0, 0, 0)
            else:
                if hand.grab_strength > 0.90:
                    # 握りこぶし
                    point_move_scroll(self, finger)
                elif hand.pinch_strength > 0.9:
                    # 親指との距離
                    # point_move_scroll(self, finger)
                    pass
                else:
                    point_move_mouse(self, normalizedPosition)


def main():
    listener = Finger_Mouse()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        # C-c or C-z
        sys.exit()
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    main()
