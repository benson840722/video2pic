import cv2
import os
import glob

# 變更到指定尺寸，長寬邊不足者補黑色
def process_image(img, min_side = 608):
    size = img.shape
    h, w = size[0], size[1]
    scale = max(w, h) / float(min_side)
    new_w, new_h = int(w/scale), int(h/scale)
    resize_img = cv2.resize(img, (new_w, new_h),cv2.INTER_AREA) # 變更尺寸
    if new_w % 2 != 0 and new_h % 2 == 0:
        top, bottom, left, right = (min_side-new_h)//2, (min_side-new_h)//2, (min_side-new_w)//2 + 1, (min_side-new_w)//2
    elif new_h % 2 != 0 and new_w % 2 == 0:
        top, bottom, left, right = (min_side-new_h)//2 + 1, (min_side-new_h)//2, (min_side-new_w)//2, (min_side-new_w)//2
    elif new_h % 2 == 0 and new_w % 2 == 0:
        top, bottom, left, right = (min_side-new_h)//2, (min_side-new_h)//2, (min_side-new_w)//2, (min_side-new_w)//2
    else:
        top, bottom, left, right = (min_side-new_h)//2 + 1, (min_side-new_h)//2, (min_side-new_w)//2 + 1, (min_side-new_w)//2
    pad_img = cv2.copyMakeBorder(resize_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0,0,0]) 
    return pad_img

# 讀寫目錄
inputPath = "/home/benson/Desktop/fake_mango/farview_video"
outputPath = "/home/benson/Desktop/fake_mango/farview_pic"

files = os.path.join(inputPath,'*.mp4')
files_grabbed = []
files_grabbed.extend(sorted(glob.iglob(files)))

for videoId in range(len(files_grabbed)):
	print(files_grabbed[videoId])
	raw = cv2.VideoCapture(files_grabbed[videoId])
	fIndex = 1
	fCount = 0

	while 1:
    # 影片轉圖片
	    ret,frame = raw.read()
	    fCount += 1
	    if (ret == True) :
	    	if (fCount % 10) == 0:
		    	img_pad = process_image(frame, min_side = 608)
		    	cv2.imwrite('%s/%02d-frame-608x608-%04d.jpg' % (outputPath, videoId,fIndex), img_pad)
		    	fIndex += 1
	    else:
	    	break
