chap0x01 基于VirtualBox的网络攻防基础环境搭建实例讲解

一、实验要求
节点：靶机、网关、攻击者主机
连通性：
靶机可以直接访问攻击者主机
攻击者主机无法直接访问靶机
网关可以直接访问攻击者主机和靶机
靶机的所有对外上下行流量必须经过网关
所有节点均可以访问互联网
其他要求 
所有节点制作成基础镜像（多重加载的虚拟硬盘）

二、实验过程：
1.构建网络拓扑
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91.png)

2.实验环境：
Victim: kali-linux-2018.3-amd64.iso   
Gateway: kali-linux-2018.3-amd64.iso   
Attacker: kali-linux-2018.3-amd64.iso   

配置一块安装了kali的 .vdi 硬盘多重加载，并在virtualbox中新建三台虚拟机，分别设置为攻击者、网关、靶机

先释放.vdi 硬盘，将该硬盘的类型改为多重加载，然后新建虚拟机时选用多重加载的虚拟硬盘。
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/2.png)

3.网络配置：
  攻击者主机和网关的一个端口在同一个网段
  靶机和网关的另一个端口在同一个网段
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85ip%E9%85%8D%E7%BD%AE.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3ip%E9%85%8D%E7%BD%AE.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BAip%E9%85%8D%E7%BD%AE.png)

4、开启网关ipv4包的转发功能，添加网关的防火墙NAT规则，设置网关转发局域网192.168.56.0/24中的数据包
在终端输入
vim /etc/sysctl.conf
添加语句
net.ipv4.ip_forward =1 sysctl -p
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/1.png)

三、实验结果
靶机可以直接访问攻击者主机
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BAping%E6%94%BB%E5%87%BB%E8%80%85%E4%B8%BB%E6%9C%BA.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BAping%E6%94%BB%E5%87%BB%E8%80%85%E7%9B%91%E5%90%AC.png)

攻击者主机无法直接访问靶机
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85ping%E9%9D%B6%E6%9C%BA.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85ping%E9%9D%B6%E6%9C%BA%E7%9B%91%E5%90%AC.png)

网关可以直接访问攻击者主机和靶机
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3ping%E6%94%BB%E5%87%BB%E8%80%85.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3ping%E6%94%BB%E5%87%BB%E8%80%85%E7%9B%91%E5%90%AC.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3ping%E9%9D%B6%E6%9C%BA.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3ping%E9%9D%B6%E6%9C%BA%E7%9B%91%E5%90%AC.png)

攻击者主机和靶机可以ping网关
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85ping%E7%BD%91%E5%85%B3.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85ping%E7%BD%91%E5%85%B3%E7%9B%91%E5%90%AC.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BAping%E7%BD%91%E5%85%B3.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BAping%E7%BD%91%E5%85%B3%E7%9B%91%E5%90%AC.png)
靶机的所有对外上下行流量必须经过网关
  靶机的网关ip 被设置为网关 eth0 的ip，靶机本身不能上网，靶机只能经网关对外访问。

所有节点均可以访问互联网
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85%E5%8F%AF%E4%B8%8A%E7%BD%91.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3%E5%8F%AF%E4%B8%8A%E7%BD%91.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BA%E8%83%BD%E4%B8%8A%E7%BD%91.png)

问题：刚开始靶机无法上网，后来更改了靶机的DNS就可以了

参考资料 
iptables使用手册 http://ipset.netfilter.org/iptables.man.html