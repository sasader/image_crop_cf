import cv2
import easygui
import os
import numpy as np

# crop size in square
size = 400
#a ratio to display big images on the screen
resize_ratio = 4
# bbox line width
linewidth = 2
# 影像資料夾，先設好就不用每次去選，但fileopenbox是獲取default那一層，所以加上*.jpg，獲取資料夾下所有jpg檔
raw_image_path = r"C:\Users\user\Desktop\try\original\*.jpg" #file path of all original images
save_path = r"C:\Users\user\Desktop\try\crop" #path to save cropped images (recommend: empty)

#https://blog.csdn.net/weixin_42118374/article/details/100176869
def cv_imread(filePath):
    cv_img=cv2.imdecode(np.fromfile(filePath,dtype=np.uint8),-1)
    # >0 Return a 3-channel color image. ， =0 Return a grayscale image. ， <0 Return the loaded image as is (with alpha channel).

    # imdecode读取的是rgb，如果后续需要opencv处理的话，需要转换成bgr，转换后图片颜色会变化
    # cv_img=cv2.cvtColor(cv_img,cv2.COLOR_RGB2BGR)
    return cv_img

# 寫入中文路徑
def cv_imwrite(filePathName, img):
    try:
        _, cv_img = cv2.imencode(".jpg", img)[1].tofile(filePathName)
        return True
    except:
        return False

# 滑鼠的callback function，(event, x, y, flags, param)這是固定寫法

# 這裡寫的不好，有機會再改
def resize_img(im):
    width = im.shape[0] #這是int
    height = im.shape[1]
    im2 = cv2.resize(im, (height // resize_ratio, width // resize_ratio), interpolation=cv2.INTER_AREA)
    return im2
    

def click_and_crop(event, x, y, flags, param):
    
    #白色框框瞄準用
    if event == cv2.EVENT_MOUSEMOVE:
        drawed_image2 = param['drawed_image'].copy()
        cv2.rectangle(drawed_image2, (x,y) , (x + (size//resize_ratio), y + (size//resize_ratio)), (255,255,255), linewidth)
        cv2.imshow('Image', drawed_image2)    
    
    # 如果點擊滑鼠左鍵
    elif event == cv2.EVENT_LBUTTONDOWN:
        rgb, label = None, None
        # 就看現在鍵盤按的按鍵是什麼，依據鍵盤決定分類名稱和框框顏色
        #set keyboard and bbox color of each class (don't use "q")
        keyboard = cv2.waitKey(0)
        if keyboard == ord('w'):
            rgb = (255, 0, 0)
            label = 'class1' 
        elif keyboard == ord('e'):
            rgb = (0, 255, 0)
            label = 'class2' 
        elif keyboard == ord('r'):
            rgb = (0, 0, 255)
            label = 'class3' 
        elif keyboard == ord('t'):
            rgb = (255, 0, 255)
            label = 'class4' 
        elif keyboard == ord('y'):
            rgb = (255, 255, 0)
            label = 'class5' 
        # 如果不是按上面鍵就什麼事都不做，防呆
        else:
            #不是continue pass break
            return None

        # 劃框框並顯示
        cv2.rectangle(param['drawed_image'], (x, y) , (x + (size//resize_ratio), y + (size//resize_ratio)), rgb, linewidth)
        cv2.imshow('Image', param['drawed_image'])

        # 看有沒有資料夾了，沒的話建一個，然後把crop的影像存進去，按照count命名
        os.makedirs(f'{param["save_path"]}/{label}', exist_ok=True)
        # 有點長，不過存起來應該是export--12345678_0之類的
        cv_imwrite(f'{param["save_path"]}/{label}/{param["original_image_name"]}_{param["count"]}.jpg', 
                   param['original_image'][(resize_ratio*y):(resize_ratio*y + size), (resize_ratio*x):(resize_ratio*x + size)])
        param["count"] += 1
        
# 用while迴圈一直讀，可一直選不同影像來crop

while True:
    
    # 取得點選資料夾的filename，會有視窗叫你選檔案，並返回檔案路徑，確認過了，沒有能記錄上次選的位置的屬性
    filename = easygui.fileopenbox(default = raw_image_path)
    
    raw_image_path = filename
    
    if not raw_image_path == None:
        #取得檔名
        original_image_name = filename.split('\\')[-1]
    
        #並去.jpg
        original_image_name = original_image_name.split('.')[0]
        
        # 讀取影像
        original_image = cv_imread(filename)
        # 壓進螢幕
        resized_original_img = resize_img(original_image)
        # 複製一個影像拿來畫框框
        drawed_image = resized_original_img.copy()
    
        # 計算crop數用，取名用
        crop_count = 0
    
        # 命名一個opencv視窗，1是autosize
        cv2.namedWindow('Image',1)
        # 把滑鼠callback指定給剛命名的視窗，https://blog.51cto.com/devops2016/2084084，建了一個字典傳給def，呼叫綠字會叫出白字
        cv2.setMouseCallback('Image', click_and_crop, param={'original_image_name': original_image_name, 'original_image': original_image, 'drawed_image': drawed_image,
                                                             'count': crop_count, 'save_path': save_path})
        # 用這個視窗顯示讀進來的影像
        cv2.imshow('Image', resized_original_img)
    
        # 如果按q就關閉視窗(如果不是按q就持續迴圈)，準備進入下一次回圈開另一個影像
        while cv2.waitKey(0) != ord('q'):
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        """     
        #如果有畫框框就存檔，只要有一個像素的!=返回True，.any()就會返回True
        if ((drawed_image != original_image).any()) :
        # 進入下一個迴圈前，把劃框框的大影像存起來，這裡{}內呼叫的是變數not字典
            cv_imwrite(f'{save_path}/{patient_directory}/{original_image_name}.jpg', drawed_image)         
        """
    #打叉關閉
    else :
        break