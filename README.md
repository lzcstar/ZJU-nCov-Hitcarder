# ZJU-nCov-Hitcarder

浙大nCov肺炎健康打卡定时自动脚本

 - 可定时，默认为每天6点5分
 - 默认每次提交上次所提交的内容（只有时间部分更新）
 
 项目用于学习交流，仅用于各项无异常时打卡，如有身体不适等情况还请自行如实打卡~
 
<img src="https://github.com/Tishacy/ZJU-nCov-Hitcarder/raw/master/demo.png" width="500px"/>

> 增加了各操作系统的phantomjs和自动选driver的功能，结果导致库变得较大，如果想自行下载对应版本的phantomjs，可以切换到`neat`分支（只保留了windows系统的phantomjs）下载本项目。

## Usage

1. clone本项目，并cd到本目录
    ```bash
    $ git clone https://github.com/Tishacy/ZJU-nCov-Hitcarder.git
    $ cd ZJU-nCov-Hitcarder
    ```
    
2. 安装依赖

    ```bash
    $ pip3 install -r requirements.txt
    ```

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



