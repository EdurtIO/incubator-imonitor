# iMonitor

iMonitor是一套服务，资源监控系统。

#### 技术架构

---

- Python3
- Flask
- Echarts
- Web Terminal

#### 支持服务

---

- Apache Druid监控
- System Memory
- System CPU

#### Contact us

---

#### 二次开发

---

- 安装外部依赖包

```bash
cnpm install -g less
```
或者
```bash
npm install -g less
```

- 克隆源码

```bash
git clone https://github.com/EdurtIO/incubator-imonitor.git
```

- 安装服务依赖

```bash
cd incubator-imonitor
pip install -r agent/src/main/python/requirements.txt
```

- 构建数据表关系（登录至MySQL服务器中执行）

```bash
source agent/src/main/python/sql/init.sql
```

- 启动服务

```bash
python agent/src/main/python/Application.py
```

- Web UI

```bash
http://localhost:5000
```
