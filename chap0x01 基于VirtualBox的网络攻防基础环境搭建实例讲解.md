# chap0x01实验报告

## chap0x01 基于VirtualBox的网络攻防基础环境搭建实例讲解 
    
 - 节点：靶机、网关、攻击者主机
    
    - 连通性
        - 靶机可以直接访问攻击者主机
        - 攻击者主机无法直接访问靶机
        - 网关可以直接访问攻击者主机和靶机
        - 靶机的所有对外上下行流量必须经过网关
        - 所有节点均可以访问互联网
    - 其他要求
        - 所有节点制作成基础镜像（多重加载的虚拟硬盘）
        
        

##### 实验过程

### 网络拓扑

![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91.png)

### 网络配置

- 靶机和网关的一个端口在同一个网段
- 攻击者主机和网关的另外一个端口在同一个网段


### 虚拟硬盘多重加载

- 安装完虚拟机后，本想将系统更新并安装增强功能，但弄了很久没有安装成功
- 将虚拟机关机，打开虚拟介质管理，将虚拟机的vdi先释放，再改为多重加载  
 - 重建三台虚拟机，选择虚拟硬盘时直接选择现有的多重加载硬盘
    
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/2.png)

### 靶机

- 使用一块网卡，选择内网模式（internal network）

![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BAip%E9%85%8D%E7%BD%AE.png)


### 网关
    
- 两块网卡，一个位内网模式，另一块为NAT network模式

![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3ip%E9%85%8D%E7%BD%AE.png)

### 攻击者

 -选择一块网卡，NAT network模式
 - 和网关的另外一个端口在同一个网段

![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85ip%E9%85%8D%E7%BD%AE.png)

### 连通测试

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

所有节点均可以访问互联网
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E6%94%BB%E5%87%BB%E8%80%85%E5%8F%AF%E4%B8%8A%E7%BD%91.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E7%BD%91%E5%85%B3%E5%8F%AF%E4%B8%8A%E7%BD%91.png)
![](https://github.com/CUCCS/2018-NS-Public-PWHL/blob/NS_chap0x01/chap0x01%E6%88%AA%E5%9B%BE/%E9%9D%B6%E6%9C%BA%E8%83%BD%E4%B8%8A%E7%BD%91.png)

靶机的所有对外上下行流量必须经过网关 靶机的网关ip 被设置为网关 eth0 的ip，靶机本身不能上网，靶机只能经网关对外访问。

问题：刚开始靶机无法上网，后来更改了靶机的DNS就可以了

参考资料 iptables使用手册 http://ipset.netfilter.org/iptables.man.html
