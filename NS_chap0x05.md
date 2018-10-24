## 局域网主机扫描
###  chap0x05 自己动手编程实现并讲解TCP connect scan/TCP stealth scan/TCP XMAS scan/UDP scan 

#### 网络拓扑
- 使用实验一网络拓扑

![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91.png)
#### 实验步骤
##### TCP connect scan
- 原理：TCP连接是客户端和服务器之间的三次握手，握手成功即可建立通信。客户端先发送设置了SYN标志的TCP 数据包和它想要连接的端口（本实验用80端口）来初始化连接，如果80端口在服务器上打开，并且接受连接，服务器给客户端发送带有SYN和ACK标志的数据包进行响应，最终由客户端发送ACK和RST标志来建立。
- [TCP connect scan 代码](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/TCP_connect_scan.py)
  - 查看端口原始状态 nmap 192.168.56.2
  
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_connect_scan1.png)
  - 在网关运行TCP_connect_scan.py，在靶机抓包，保存在test1.pcap中，用wireshark打开查看抓包情况
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_connect_scan2.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_connect_scan3.png)
  - 在靶机开启apache服务，查看靶机的80端口状态，处于监听状态
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_connect_scan4.png)	
  - 在网关运行TCP_connect_scan.py，输出结果80端口处于打开状态，在靶机捕获的数据包也有TCP三次握手
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_connect_scan5.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_connect_scan6.png)

##### TCP stealth scan
- TCP隐形扫描和TCP连接扫描相类似，客户端发送TCP数据包，包含SYN标志和目的端口号，如果端口打开，服务器将使用TCP数据包内的SYN和ACK响应，最终客户端发送的是RST标志
- [TCP stealth scan代码](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/TCP_stealth_scan.py) 
  - 端口关闭时收到的包
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_stealth_scan1.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_stealth_scan2.png)
  - 打开端口收到的包
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_stealth_scan4.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_stealth_scan3.png)

##### TCP xmas_scan
- 在XMAS扫描中，将设置了FIN、PSH、URG标志的TCP数据包以及要连接的目的端口号发送到服务器，如果服务器响应TCP数据包内置的RST标志，则端口为关闭状态。如果端口已经打开，服务器将不会响应
- [TCP xmas_scan代码](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/TCP_xmas_scan.py)
  - 端口处于关闭和打开状态分别在网关运行tcp_xmas_scan.py
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_xmas_scan1.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_xmas_scan2.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_xmas_scan3.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/tcp_xmas_scan4.png)

#### UDP scan
- 客户端发送一个包含连接端口的UDP数据包，如果端口打开，服务器会给予响应。若服务器端口响应ICMP端口不可达错误类型3，则端口处于关闭状态
- [UDP scan代码](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/UDP_scan.py)
  - 端口关闭时抓包，可以看到显示错误类型3
 ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/UDP_scan1.png)
 ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/UDP_scan2.png)
  - 端口开启时抓包
    - 用echo -n "20181024" | nc –nvulp 53开启端口
    - 用nmap –sU ip –p 端口号查看53端口的状态
    - nc指令默认打开的是tcp的端口，执行完开启端口的指令后，再执行下一条指令时udp 53端口就会关闭掉，抓不到想要的包，所以先打开抓包，再打开端口，再执行UDP_scan.py
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/UDP_scan3.png)
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x05/ns5_picture/UDP_scan4.png)