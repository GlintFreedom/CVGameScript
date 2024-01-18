## 《开局托儿所》脚本

> 谨防资本主义腐蚀，用AI战胜资本主义陷阱！

##### 运行配置

1. 下载*Tesseract-OCR*并记录安装位置

   找到自己需要的版本：https://digi.bib.uni-mannheim.de/tesseract/

2. 根据实际情况补全*Tesseract-OCR*位置

   ```python
   os.environ['TESSDATA_PREFIX'] = r'D:\Tesseract-OCR'  # 替换为您的实际路径
   pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'  # 替换为您的实际路径
   ```

3. 安装*requirements.txt*所需依赖

   ```shell
   pip install -r requirements.txt
   # conda install --yes --file requirements.txt
   ```

##### 运行步骤

1. PC端使用微信打开“开局托儿所”小程序

2. 点击“开始挑战”后，等页面稳定倒计时后，再运行脚本*operateWin.py*

3. 大约据倒计时结束$\frac{2}{3}$到$\frac{1}{2}$时，开始自动消除

4. 由于每局会随机进入死局，分数不固定，因此程序运行后会自动等待本局结束，并自动开始下一局游戏，反复自动化刷分

   **注意：需要提前看完3次广告获得无限挑战能力才可以，否则无法自动开始下一局游戏**

5. 按`ctrl+C`、`ctrl+Z`等快捷键停止运行



#### 祝愿人人都能上学 ᕙ(`▿´)ᕗ

