## 实战Bro网络入侵取证
### 实验环境
- 安装bro
```
apt-get install bro bro-aux
``` 
- 实验环境基本信息
```
lsb_release -a
uname -a
bro -v
```
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro1.png)
### 编辑bro配置文件
- 编辑```/etc/bro/site/local.bro```，在文件尾部追加两行代码
```
#提取所有文档
@load frameworks/files/extract-all-files
#加载脚本
@load mytuning.bro
```
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro2.png)
- 在```/etc/bro/site/```目录下创建新文件，添加内容
```
redef ignore_checksums = T;
```
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro3.png)
### 使用bro自动化分析pcap包
- 执行
```
bro -r attack-trace.pcap /etc/bro/site/local.bro
```
- 出现警告信息
```
WARNING: No Site::local_nets have been defined.  It's usually a good idea to define your local networks.
```
- 对于本次实验没有影响，要解决上面的警告信息，需要编辑```mytuning.bro```，增加一行变量定义
```
redef Site::local_nets = { 192.150.11.0/24 };
```
- 加入上述变量定义后，再运行指令，警告信息就没有了
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro4.png)
- 而且还生成了```extract_files``` 目录和两个日志文档```known_hosts.log```和```known_hosts.log```，这两个日志文档会报告在当前流量中发现了本地网络IP和IP关联的已知服务信息
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro5.png)
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro6.png)
- ```extract_files ```目录中有一个文件，将其上传到
[virustotal](https://www.virustotal.com/#/home/upload),发现它是已知的后门程序，基于这个发现就可以进行逆向倒推，寻找入侵线索。
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro8.png)
- 阅读```/usr/share/bro/base/files/extract/main.bro```的源代码，可以了解到文档名的最右一个右侧对应的字符串```FHUsSu3rWdP07eRE4l```是files.log中的文档唯一标识
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro7.png)
- 通过查看files.log，发现该文件提取自网络会话标识为CJcQwXlwZMUh1HHtI8的FTP会话
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro9.png)
- CJcQwXlwZMUh1HHtI8会话标识在```conn.log```中可以找到对应的IP五元组信息
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro10.png)
- 通过conn.log的会话标识匹配，我们发现该PE文件来自于IP地址为```98.114.205.102```的主机。
### Bro的其他一些技巧
- 显示捕获的FTP登录口令
  - ftp.log中默认不会显示捕获的FTP登录口令，可以通过在```/etc/bro/site/mytuning.bro``` 中增加以下变量重定义来实现
  ```
  redef FTP::default_capture_password = T;
  ```
  - 添加代码前
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro11.png)
  - 添加代码后（刚开始添加完后，hidden没有变为1，做下面的SMB识别，更改了local.bro，再执行```bro -r attack-trace.pcap /etc/bro/site/local.bro```后，hidden变为1）（问了其他同学她们是加了```redef FTP::default_capture_password = T;```就直接看到hidden->1的结果）
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro12.png)
- SMB协议识别  
  - 编辑```/etc/bro/site/local.bro```，添加``` @load protocols/smb```，对比```known_services.log```，发现能够识别出SMB流量
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro13.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x12/picture/bro14.png)
### 参考资料
- [基于bro的计算机网络入侵取证](https://hk.saowen.com/a/97a775209136d0955c5d4a6476ff88658207066ca5a1d94e63baffb024626619)
- [计算机取证实验](https://sec.cuc.edu.cn/huangwei/textbook/ns/chap0x12/exp.html)
- [2018-NS-Public-Lyc-heng](https://github.com/CUCCS/2018-NS-Public-Lyc-heng/blob/ns_chap0x12/ns_chap0x12/%E5%AE%9E%E9%AA%8C%E6%8A%A5%E5%91%8A.md)