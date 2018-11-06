*IP_Pool / IP_Proxy*
===
## <font color=red>*WARRING:*</font>
#### <font color=red>*1. 所抓取代理大多数为HTTP，请不要用于请求需要账号密码的站点，避免密码泄露。*</font>
#### <font color=red>*2. 请合理使用于私人项目或个人学习，禁止用于商业用途及任何违法违规的场景。*</font>

## 简述及建议：
用于从公开网站抓取高匿代理ip，验证后以json格式保存到本地文件中，并进行周期性验证，同时提供api接口。
* 采用本地json文件保存，未配置数据库。
* 需要设置其它源只需在 `ip_crawl`中新增爬虫类即可；有其它需求字段可自行添加到 `items` 及爬虫代码中。
* 日志在终端过滤等级设置为 `INFO`，如需查看更详细的日志请在log.yml中将终端过滤等级配置为 `DEBUG`。
* <font color=red>***建议保持目前的抓取速率或更慢***</font>，过快的抓取速度除了徒增他人服务器压力外无任何其它帮助(源更新速度有限)。
* <font color=red>***文件相对路径请不要随意更改***</font>，如有需要更改后根据报错信息到相关文件中修改相对路径。
* 由于爬虫代码具有时效性，<font color=red>***如代理池运行中提示爬虫代码错误，请优先排查是否源网页结构已经发生改变***。</font>
* 所使用网站信息：
    * *验证网站: http://www.httpbin.org/ip*
    * *西刺代理: http://www.xicidaili.com/*
    * *快代理: https://www.kuaidaili.com/free/*

## 使用方式：
* 启动 `run.py`，此时同时启动了爬虫及周期性验证程序，有效数据会自动写入文件 `/data/ip_data.json`
* 【可选】启动 `api.py`，利用api获取单个有效ip。 
* 【可选】在需要使用程序中导入 `tool_lib`，使用 `tool_lib.get_valid_ip()` 获取单个有效ip。
* 【可选】直接打开储存文件 `ip_data.json` 手动使用


## API：
#### *以127.0.0.1:5000为例:*
    获取单个有效ip(有验证):    127.0.0.1:5000/ip_pool/api/v1.0/get_ip
    查看文件中所有ip(无验证):  127.0.0.1:5000/ip_pool/api/v1.0/get_ip_pool
    查看文件中指定ip(无验证):  127.0.0.1:5000/ip_pool/api/v1.0/get_a_ip/0


## 文件说明：
    --[ip_pool]:          
        --[pool]
            --[core]:
                --ip_crawl.py           # 爬虫代码
                --tool_lib.py           # 工具函数集合    
            --items.py              # 数据结构定义文件
            --settings.py           # 基础设置文件
            --api.py                # RESTful API接口文件

        --[data]:
            --ip_data.json          # 有效ip存储文件（运行后生成文件夹）
        --[log]:
            --err.log               # 错误日志（运行后生成文件夹）
            
        --run.py                # 爬虫及验证程序启动文件
        --log.yml               # logging配置文件
        --requirements.txt      # python requirments
        --README.md    
 ## 博客地址：
 [用Python搭建高匿代理IP池](https://)
