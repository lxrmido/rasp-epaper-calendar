# rasp-epaper-calendar

一个在树莓派+微雪4.2寸墨水屏上绘制日历的例子

这是一个基于 https://github.com/lxrmido/node-paper-calendar 的示例，原理为每五分钟读取一次图片然后渲染到屏幕

运行前请确保已经安装`python3`及相关的库：

`pip3 install SPI`

`pip3 install Pillow`

有时可能还要手动安装`RPi.GPIO`

`pip3 install RPi.GPIO`

然后在此项目根目录下建立一个 `config.ini` , 填入 `node-paper-calendar`的URL：

```
[url]
image=http://127.0.0.1:4001/calendar?width=400&height=300
```

最后，运行：

`python3 getimage.py`

当然，你也可以装个`screen`去运行

如果你用的是其他型号的微雪SPI墨水屏，把相应的库加入lib文件夹再把代码中的epd4in2更改掉即可