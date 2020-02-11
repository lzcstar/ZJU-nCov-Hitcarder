# ZJU-nCov-Hitcarder

浙大nCov肺炎健康打卡定时自动脚本

 - 可定时，默认为每天6点5分
 - 默认每次提交上次所提交的内容（只有时间部分更新）
 
 项目用于学习交流，仅用于各项无异常时打卡，如有身体不适等情况还请自行如实打卡~
 
<img src="https://github.com/Tishacy/ZJU-nCov-Hitcarder/raw/master/demo.png" width="500px"/>



## Usage

1. clone本项目，并cd到本目录
    ```bash
    $ git clone https://github.com/Tishacy/ZJU-nCov-Hitcarder.git
    $ cd ZJU-nCov-Hitcarder
    ```
    
2. 安装依赖

   需要安装的依赖分为python包和phantomjs两部分。
   1. 安装依赖的python包
       ```bash
       $ pip3 install -r requirements.txt
       ```
       
   2. 安装对应操作系统版本的phantomjs。

       该分支下中默认存在windows版本的phantomjs。其他对应操作系统的phantomjs可在 [https://phantomjs.org/download.html](https://phantomjs.org/download.html) 下载，并将下载后解压的到`phantomjs`文件（一般在`/bin`目录下）复制到本项目目录，并按如下方式命名即可：
       - macOS: 命名为`phantomjs-mac`
       - linux(64位): 命名为`phantomjs-linux`

3. 将config.json.templ模板文件重命名为config.json文件，并修改 config.json中的配置
    
    ```javascript
    {
        "username": "你的浙大统一认证平台用户名",
        "password": "你的浙大统一认证平台密码",
        "schedule": {
            "hour": "6",    // 6点
            "minute": "5"   // 5分 
        }
    }
    ```

4. 启动定时自动打卡脚本

   ```bash
   $ python3 daka.py
   ```



## Tips

- 为了防止电脑休眠或关机时程序不运行，推荐把这个部署到VPS上



## LICENSE

Copyright (c) 2020 tishacy.

Licensed under the [MIT License](https://github.com/Tishacy/ZJU-nCov-Hitcarder/blob/master/LICENSE)



