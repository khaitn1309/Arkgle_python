import os

# def list_files(startpath):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))

# path = r'C:\Users\user\Downloads'
# path = (path.replace('user', os.getlogin()))
# list_files(path)

path = r'C:\Users\user\Downloads'
path = (path.replace('user', os.getlogin()))
list_dir_file = os.listdir(path)
for item in list_dir_file:
    print (item)
