#ALPR
def main():
    import cv2
    import csv
    import imutils
    import numpy as np
    import pytesseract
    from PIL import Image
    counter = 1
    while True:
        img = cv2.imread(f"car{counter}.jpg",1)
        img = imutils.resize(img,width = 500) # preserve the original aspect ratio of image
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grey = cv2.bilateralFilter(grey,11,17,17)
        canny = cv2.Canny(grey,30,200)
        contours,op = cv2.findContours(canny.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours,key = cv2.contourArea,reverse=True)[:30]
        numplate = None
        idx=1
        loc = ""
        for c in contours:
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * peri, True)
            if len(approx) == 4:
                numplate = approx
                x,y,w,h = cv2.boundingRect(c)
                new_img=img[y:y+h,x:x+w]
                loc = "./"+str(idx)+".jpg"
                cv2.imwrite(loc,new_img)
                idx += 1
                break
        cv2.drawContours(img, [numplate], -1, (0, 255, 0), 3)
        cv2.imshow("Plate",new_img)
        cv2.waitKey(0)
        text=pytesseract.image_to_string(loc,lang='eng') #converts image characters to string
        print("Number is:" ,text)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        name = input("Enter name: ")
        number = int(input("Enter phone number: "))
        aadhar = int(input("Enter aadhar number: "))
        address = input("Enter your address: ")
        with open("details.csv",'a') as file:
            writer = csv.writer(file)
            row = [name,str(number),aadhar,address,text]
            writer.writerow(row)
        forward = input("Do you wish to continue (Y/N)")
        if forward == "N":
            break
        else:
            counter +=1
if __name__=="__main__":
    main()
