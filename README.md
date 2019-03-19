# Leapmotion_Mouse

LeapMotionを使ってマウス操作を行うサンプル

## develop
- Win10
- Python 3.6.8
- LeapDeveloperKit_3.2.1+45911_win

## include
- You need ctypes
  ```
  $pip install pywin32
  
  $pip freeze
  pywin32==224
  ```

## LeapMotionはV4でAPIが廃止されている
- V4 SDKにはLeap.pyや、Leap.dll/LeapPython.pydが含まれない
- V3.2.1をDLしてPythonファイルとかを持ってくる
  - [SDK 3.2.1はここからDL可能](https://developer.leapmotion.com/releases/?category=orion)
- V3.2.1は古いので、Python3にする
  - [V3 Python SettingUp a Project](https://developer-archive.leapmotion.com/documentation/python/devguide/Project_Setup.html)
  - [python3化(公式からのリンク)](https://support.leapmotion.com/hc/en-us/articles/223784048)
  - [swing win](http://www.swig.org/download.html)
