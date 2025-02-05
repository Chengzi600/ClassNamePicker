<!--markdownlint-disable MD001 MD033 MD041 MD051-->

<div align="center">

# ClassNamePicker

![banner](images/classnamepicker-screenshot.png)

[![Stars](https://img.shields.io/github/stars/Chengzi600/RandomPickName?label=Stars)](https://github.com/ClassIsland/ClassIsland)
[![Release](https://img.shields.io/github/v/release/Chengzi600/RandomPickName?style=flat-square&color=%233fb950&label=正式版)](https://github.com/ClassIsland/ClassIsland/releases/latest)
[![下载量](https://img.shields.io/github/downloads/Chengzi600/RandomPickName/total?style=social&label=下载量&logo=github)](https://github.com/ClassIsland/ClassIsland/releases/latest)

[![forks](https://img.shields.io/github/forks/Chengzi600/ClassNamePicker?style=flat&color=blue)](https://github.com/Chengzi600/ClassNamePicker/forks)
[![Watchers](https://img.shields.io/github/watchers/Chengzi600/ClassNamePicker?style=flat&color=green)](https://github.com/Chengzi600/ClassNamePicker/watchers)
[![GitHub Issues](https://img.shields.io/github/issues-search/Chengzi600/ClassNamePicker?query=is%3Aopen&label=issues&color=purple)](https://github.com/Chengzi600/ClassNamePicker/issues)

![GitHub License](https://img.shields.io/github/license/Chengzi600/ClassNamePicker?color=red)

ClassNamePicker 是一款功能强大的课堂随机点名工具<br/>
使用 PyQt5 编写，界面简洁
</div>

## 功能

> [!TIP]
>
> 新功能持续开发中，可能不及时同步在此 README 中，请以 Release 日志为准

### 基础抽取

- [x] 从整个班级的名单中随机抽取一人
- [x] 选择从班级的男生/女生名单中随机抽取一人
- [ ] 均衡抽取男生/女生
- [x] 可选是否允许重复抽到一人
- [x] 可保存已抽取过人的名字，并在下次打开后读取

### 互动玩法

- [x] 最小化后显示悬浮窗，可快速从课件切换
- [x] 抽取一人后自动开启计时器，适用于限时背诵等场景
- [x] 语音播报抽到人的名字
- [x] 统计已抽人数、剩余人数、概率、总抽取次数等信息
- [x] 简易的抽取动画，可在配置文件中自定义时长

### 名单编辑

- [x] 读取 TXT 文件，每行一个名字，支持从表格中直接复制名字一列
- [x] 只需再编辑女生名字，即可自动算出男生名字列表
- [ ] ……

## 开始使用
### 首次安装
**首先，请确保您的设备满足以下推荐需求：**

- Windows 系统

> 强烈建议在 Github Releases 下载，仅在它难以连接时选择其它渠道，因为其他渠道往往更新不及时

|      下载渠道      | **🚀 正式版**<br/>[![正式版](https://img.shields.io/github/v/release/Chengzi600/ClassNamePicker?style=flat-square&color=%233fb950&label=)](https://github.com/Chengzi600/ClassNamePicker/releases/latest) |                                       🚧 测试版<br/>                                       |
|:--------------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|:---------------------------------------------------------------------------------------:|
| GitHub Release |                                                               [**下载**](https://github.com/Chengzi600/ClassNamePicker/releases/latest)                                                               | 在 [Actions](https://github.com/Chengzi600/ClassNamePicker/actions) 中寻找或自行从`develop`分支构建 |
|      蓝奏云盘      |                                                                                                暂未上传                                                                                                 |                                            -                                            |


下载完成后，将软件压缩包解压，解压时请不要解压到C盘根目录、【下载】文件夹中，否则可能会出现**文件无法读写、文件丢失**等问题

先启动一次程序，然后进入同级目录下`PickNameConfig`文件夹，编辑`names.txt`，每行填写一个名字，不要有空行（可从含有学生名字的表格中直接复制名字一列），然后可选择编辑`g_names.txt`，即为女生名单，男生名单将自动算出

如您有 Python 环境，可以直接拉取项目，安装依赖（`pip install -r requirements.txt`）并运行`ClassNamePicker.py`，速度更快

### 升级教程
 **一般来说，直接将新版本解压，然后将旧版本的配置文件夹`PickNameConfig`复制到解压出来的文件夹内即可** 

若一切正常，程序将提示配置文件更新成功

若不慎损坏配置文件，则需要手动删除软件配置文件`config.json`，总抽取次数和上次保存记录将丢失

## 获取帮助

如果您确定遇到的问题是一个 **Bug**，或者要提出一项**新的功能**，请提交 Issue

或联系作者: **QQ:2752718571**

## 开发

本项目目前开发状态：

- 正在 [`develop`](https://github.com/Chengzi600/ClassNamePicker/tree/develop) 分支上开发新版本和维护旧版本
- [`master`](https://github.com/Chengzi600/ClassNamePicker/tree/master) 推送可正常使用的版本


要在本地编译应用，您需要安装以下负载和工具：

- Python 3.9
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
