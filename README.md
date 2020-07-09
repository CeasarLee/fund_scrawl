# fund_scrawl
   fund scrawl是一个爬取天天基金网上所有基金历年数据的爬虫，为了共同富裕，大家可以尽情使用。希望大家可以多多start，fork啦！
   
## Table of Contents

- [Background](#background)
- [Requirement](#requirement)
- [Usage](#usage)

## Background
这段时间基金暴涨，人人都可以当股神的时期又来啦，希望大家能够通过这个git，找到可以穿越牛熊的基金。

## Requirement
python 3.5
requests
threading(如果希望多线程）
Beautiful soup4
## Usage
通过修改main.py 里面的start date， end date，save path来得到自己需要的起始时间，以及保存路径。
现在的爬取方法是爬取数据后等待来完成的，如果希望通过采用ip池的方法进行数据的爬取可以参考这个git [proxy_pool](https://github.com/jhao104/proxy_pool)来进行搭建。
个人尝试过了好几个免费的代理，代理的质量都不高，如果希望采用代理进行数据爬取的加速，将爬虫中的load_data函数改为load_data_ip即可，通过改写get_proxy函数来进行自己ip池的设置，如果有问题就issue我吧～
