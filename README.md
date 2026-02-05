<!--markdownlint-disable MD001 MD033 MD041 MD051-->

<div align="center">

# ClassNamePicker


[![Stars](https://img.shields.io/github/stars/Chengzi600/RandomPickName?label=Stars)](https://github.com/ClassIsland/ClassIsland)
[![Release](https://img.shields.io/github/v/release/Chengzi600/RandomPickName?style=flat-square&color=%233fb950&label=正式版)](https://github.com/ClassIsland/ClassIsland/releases/latest)
[![下载量](https://img.shields.io/github/downloads/Chengzi600/RandomPickName/total?style=social&label=下载量&logo=github)](https://github.com/ClassIsland/ClassIsland/releases/latest)

[![forks](https://img.shields.io/github/forks/Chengzi600/ClassNamePicker?style=flat&color=blue)](https://github.com/Chengzi600/ClassNamePicker/forks)
[![Watchers](https://img.shields.io/github/watchers/Chengzi600/ClassNamePicker?style=flat&color=green)](https://github.com/Chengzi600/ClassNamePicker/watchers)
[![GitHub Issues](https://img.shields.io/github/issues-search/Chengzi600/ClassNamePicker?query=is%3Aopen&label=issues&color=purple)](https://github.com/Chengzi600/ClassNamePicker/issues)

![GitHub License](https://img.shields.io/github/license/Chengzi600/ClassNamePicker?color=red)

ClassNamePicker 是一款轻量的课堂随机点名工具<br/>
使用 PyQt5 编写，开箱即用，配置便捷
</div>

## 功能

> [!TIP]
>
> 新功能持续开发中，可能不及时同步在此 README 中，请以 Release 日志为准

### 基础抽取

- [x] 从整个班级的名单中随机抽取一人
- [x] 选择从班级的男生/女生名单中随机抽取一人
- [x] 可选是否允许重复抽到一人(放回/不放回抽取)
- [x] 可保存已抽取过人的名字，并在下次打开后读取

### 互动玩法

- [x] 显示置顶悬浮窗，可快速从课件切换(悬浮窗可自定义大小)
- [x] 抽取一人后自动开启计时器，适用于限时背诵等场景
- [x] 语音播报抽到人的名字
- [x] 显示已抽人数、剩余人数、概率、总抽取次数等信息
- [x] 简易抽取动画

### 名单编辑与维护

- [x] 直接读取 TXT 文件，每行一个名字，可从现有表格中直接复制名字一列
- [x] 只需编辑女生名字，即可自动算出男生名字列表
- [x] 便捷简单的配置面板
- [x] 有效反制希沃管家弹窗拦截
- [ ] ……

## 开始使用
### 首次安装
**首先，请确保您的设备满足以下推荐需求：**

- Windows 系统

> 强烈建议在 Github Releases 下载，仅在它难以连接时选择其它渠道，因为其他渠道往往更新不及时

|      下载渠道      | **🚀 正式版**<br/>[![正式版](https://img.shields.io/github/v/release/Chengzi600/ClassNamePicker?style=flat-square&color=%233fb950&label=)](https://github.com/Chengzi600/ClassNamePicker/releases/latest) |                                     🚧 测试版<br/>                                     |
|:--------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------------:|
| GitHub Release |                                                               [**下载**](https://github.com/Chengzi600/ClassNamePicker/releases/latest)                                                               |           [Actions](https://github.com/Chengzi600/ClassNamePicker/actions)          |


下载完成后，将软件压缩包解压，解压时请不要解压到C盘根目录、【下载】文件夹中，否则可能会出现**文件无法读写、文件丢失**等问题

启动程序，在上方工具栏打开配置面板，编辑`names.txt`(总名单)，每行填写一个名字，不要有空行（可从含有学生名字的现成表格中直接复制名字一列），然后可选编辑`g_names.txt`(女生名单)，男生名单将自动算出

如您有 Python 环境，可以直接拉取项目，安装依赖（`pip install -r requirements.txt`）并运行`ClassNamePicker.py`，速度更快

### 升级教程
 **一般来说，直接将新版本解压，覆盖即可**
如遇配置文件错误，可尝试删除`/PickNameConfig`下的`.json`文件

## 获取帮助

如果您确定遇到的问题是一个 **Bug**，或者要提出一项**新的功能**，请提交 Issue

或联系作者: **QQ:2752718571**

## 开发

本项目目前开发状态：

- 正在 [`develop`](https://github.com/Chengzi600/ClassNamePicker/tree/develop) 分支上开发新版本
- [`master`](https://github.com/Chengzi600/ClassNamePicker/tree/master) 推送可正常使用的版本


要在本地编译应用，您需要安装以下负载和工具：

- Python 3.9+
- 安装依赖（已在`requirements.txt`列出）
- 任意 IDE，如 PyCharm


如果您有意愿做出代码贡献，欢迎提交 Pull Requests，给项目一个 Star


## 许可证

本项目基于 [WTFPL License](LICENSE) 获得许可

## Stars 历史

[![Star 历史](https://starchart.cc/Chengzi600/ClassNamePicker.svg?variant=adaptive)](https://starchart.cc/Chengzi600/ClassNamePicker)

<div align="center">

如果这个项目对您有帮助，请点亮 Star ⭐

</div>
