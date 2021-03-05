# OCR LINE-Bot (Only English image)
OCR server for [LINE bot](https://developers.line.biz/ja/docs/messaging-api/) using [heroku](https://dashboard.heroku.com/apps) and tesseract.  
You can get (String)text from picture english written. 

# Requirements
* heroku account
* LINE developer account

# How to use
- You need to use tesseract-ocr at heroku so you must install tesseract-libs by apt.  
  ## install apt
  `heroku buildpacks:add --index 1 heroku-community/apt`
  
- You must set Environmental Variable to heroku.  
  1. TESSDATA_PREFIX (for tesseract)  
  `heroku config:set TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/4.00/tessdata`  
  
        #### perhaps tessdata directory is different if so, you can check by using below command
        ```
        heroku run bash     
        find -iname tessdata
        ```    

  
  2. YOUR_CHANNEL_ACCESS_TOKEN  
  `heroku config:set YOUR_CHANNEL_ACCESS_TOKEN=**YOUR TOKEN**`
  
  3. YOUR_CHANNEL_SECRET  
  `heroku config:set YOUR_CHANNEL_SECRET=**YOUR SECRET**`

- change heroku stack 20 to 18 because "tesseract-ocr 4.0" didn't work in my heroku-20.

- deploy those file
