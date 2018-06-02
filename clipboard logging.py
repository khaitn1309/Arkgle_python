import win32clipboard # pypiwin32

# set clipboard data
# win32clipboard.OpenClipboard()
# win32clipboard.EmptyClipboard()
# win32clipboard.SetClipboardText('testing 123')
# win32clipboard.CloseClipboard()

# get clipboard data
win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
print (data)

from PIL import ImageGrab
im = ImageGrab.grabclipboard()
im.save('somefile.png','PNG')