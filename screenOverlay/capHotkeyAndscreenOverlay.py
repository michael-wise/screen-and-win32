# After a post to c.l.py by Richie Hindle:
# http://groups.google.com/groups?th=80e876b88fabf6c9
import os
import sys
import ctypes
from ctypes import wintypes
import win32con #^for hotkeys
import win32api, win32con, win32gui, win32ui #for screen stuff

def main():
    hInstance = win32api.GetModuleHandle()
    className = 'MyWindowClassName'

    wndClass                = win32gui.WNDCLASS()
    wndClass.style          = win32con.CS_HREDRAW | win32con.CS_VREDRAW
    wndClass.lpfnWndProc    = wndProc
    wndClass.hInstance      = hInstance
    wndClass.hCursor        = win32gui.LoadCursor(None, win32con.IDC_ARROW)
    wndClass.hbrBackground  = win32gui.GetStockObject(win32con.WHITE_BRUSH)
    wndClass.lpszClassName  = className
    wndClassAtom = win32gui.RegisterClass(wndClass)
    exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
    style = win32con.WS_DISABLED | win32con.WS_POPUP | win32con.WS_VISIBLE
    hWindow = win32gui.CreateWindowEx(exStyle, wndClassAtom, None, # WindowName
        style, 0, 0,# x,y
        win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN), # width,height 
        None, # hWndParent
        None, # hMenu
        hInstance, None # lpParam
    )
    win32gui.SetLayeredWindowAttributes(hWindow, 0x00ffffff, 255, win32con.LWA_COLORKEY | win32con.LWA_ALPHA)
    #win32gui.UpdateWindow(hWindow)
    win32gui.SetWindowPos(hWindow, win32con.HWND_TOPMOST, 0, 0, 0, 0,
        win32con.SWP_NOACTIVATE | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)
    #win32gui.ShowWindow(hWindow, win32con.SW_SHOW)
    # win32gui.PumpMessages()

def wndProc(hWnd, message, wParam, lParam):
    if message == win32con.WM_PAINT:
        hdc, paintStruct = win32gui.BeginPaint(hWnd)
        print 'windProc'
        dpiScale = win32ui.GetDeviceCaps(hdc, win32con.LOGPIXELSX) / 60.0
        fontSize = 80
        lf = win32gui.LOGFONT()
        lf.lfFaceName = "Times New Roman"
        lf.lfHeight = int(round(dpiScale * fontSize))
        hf = win32gui.CreateFontIndirect(lf)
        win32gui.SelectObject(hdc, hf)
        rect = win32gui.GetClientRect(hWnd)
        win32gui.DrawText(hdc,'O',-1,rect,win32con.DT_CENTER | win32con.DT_NOCLIP | win32con.DT_SINGLELINE | win32con.DT_VCENTER)
        win32gui.EndPaint(hWnd, paintStruct)
        return 0
    elif message == win32con.WM_DESTROY:
        print 'Closing the window.'
        win32gui.PostQuitMessage(0)
        return 0
    else:
        return win32gui.DefWindowProc(hWnd, message, wParam, lParam)
if __name__ == '__main__':
    main()


byref = ctypes.byref
user32 = ctypes.windll.user32

HOTKEYS = {
  1 : (win32con.VK_F3, win32con.MOD_WIN),
  2 : (win32con.VK_F4, win32con.MOD_WIN)
}

def handle_win_f3 ():
  os.startfile (os.environ['TEMP'])

def handle_win_f4 ():
  user32.PostQuitMessage (0)

HOTKEY_ACTIONS = {
  1 : handle_win_f3,
  2 : handle_win_f4
}

#
# RegisterHotKey takes:
#  Window handle for WM_HOTKEY messages (None = this thread)
#  arbitrary id unique within the thread
#  modifiers (MOD_SHIFT, MOD_ALT, MOD_CONTROL, MOD_WIN)
#  VK code (either ord ('x') or one of win32con.VK_*)
#
for id, (vk, modifiers) in HOTKEYS.items ():
  print "Registering id", id, "for key", vk

  if not user32.RegisterHotKey (None, id, modifiers, vk):
    print "Unable to register id", id

#
# Home-grown Windows message loop: does
#  just enough to handle the WM_HOTKEY
#  messages and pass everything else along.
#

try:
  msg = wintypes.MSG ()
  print 'Getting list of registered hotkeys'
  while user32.GetMessageA (byref (msg), None, 0, 0) != 0:
    print 'whiling'
    if msg.message == win32con.WM_HOTKEY:
      action_to_take = HOTKEY_ACTIONS.get (msg.wParam)
      if action_to_take:
        action_to_take ()

    user32.TranslateMessage (byref (msg))
    user32.DispatchMessageA (byref (msg))
finally:
  print 'unbinding registered hotkeys'
  for id in HOTKEYS.keys ():
    user32.UnregisterHotKey (None, id)
