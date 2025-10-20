# NotosIsland

![GitHub Release](https://img.shields.io/github/v/release/doubsumi/NotosIsland?style=flat-square&logo=github)
![GitHub License](https://img.shields.io/github/license/doubsumi/NotosIsland?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-0078d7?style=flat-square&logo=windows)
![Python](https://img.shields.io/badge/Python-3.6+-3776ab?style=flat-square&logo=python)
![GitHub stars](https://img.shields.io/github/stars/doubsumi/NotosIsland?style=flat-square&logo=github)
![GitHub forks](https://img.shields.io/github/forks/doubsumi/NotosIsland?style=flat-square&logo=github)

一个轻量级的Windows桌面系统监控工具，在导航栏位置实时显示网速，核心占用等系统关键性能指标。

## ✨ 特性

- **实时系统监控** - 显示CPU、GPU、内存使用率
- **网络速度监控** - 实时显示上传/下载速度
- **温度监控** - 监控CPU和GPU温度
- **悬浮窗设计** - 无边框、半透明、始终置顶显示
- **智能交互** - 双击切换简洁/详细模式
- **低资源占用** - 轻量级设计，不影响系统性能

## 🖼️ 截图展示

### 默认模式
![默认模式](https://private-user-images.githubusercontent.com/83439590/503101139-d7ebc3eb-09db-4746-96c2-901b0aa91dc5.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjA5NDMxMTIsIm5iZiI6MTc2MDk0MjgxMiwicGF0aCI6Ii84MzQzOTU5MC81MDMxMDExMzktZDdlYmMzZWItMDlkYi00NzQ2LTk2YzItOTAxYjBhYTkxZGM1LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEwMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMDIwVDA2NDY1MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTgxYTAxMDY0N2Y3MmVjYzY4NWJkMDA5NjAwNTdmYWQxMTI4NDdiNGYxZTdhNzJkNDk4NjY3NjY5NGFjZmRhOWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.mC1siTGh83NrAW3EiMHQe4RbFSziZ3N9Axh-4dx637o)

*鼠标滚轮调整背景色深浅*

![img.png](https://private-user-images.githubusercontent.com/83439590/503100474-bcc2f67d-a6d6-4493-b086-b75c0a446dc4.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjA5NDMwMTEsIm5iZiI6MTc2MDk0MjcxMSwicGF0aCI6Ii84MzQzOTU5MC81MDMxMDA0NzQtYmNjMmY2N2QtYTZkNi00NDkzLWIwODYtYjc1YzBhNDQ2ZGM0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEwMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMDIwVDA2NDUxMVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWZjNGRmYmEyYmU5MmU5M2YxZWVlMGJlZmQ2NWJkNzQ0ZTMxOTNjN2YxZGQ2NGEyZTJjYjUyY2ZjMTUzMTY2ZDUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.ilctHQQjNVeUoz9yL4-EmE3T1HhLIMW3LDkJhBYvXd0)

*默认简洁显示模式，占用空间小*

### 详细模式  
![详细模式](https://private-user-images.githubusercontent.com/83439590/503101192-8c2995f1-6992-4a3b-b6d3-f516acdc8135.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjA5NDMxMTIsIm5iZiI6MTc2MDk0MjgxMiwicGF0aCI6Ii84MzQzOTU5MC81MDMxMDExOTItOGMyOTk1ZjEtNjk5Mi00YTNiLWI2ZDMtZjUxNmFjZGM4MTM1LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEwMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMDIwVDA2NDY1MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTY5MGRkMDA4ZmVlNjg3ZjRiNTkyMTNhNjkxN2UyOGQ4MDliN2I4NThjMmIzZjg0ODZhZjVhYmJhNjYyYzA0YTgmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.-ytBZQvzRb8ZU5twFtP1bf08leKOje_S5MupkXdOGnM)

*鼠标移动到界面后展开详细监控信息*

### 设置界面
![设置界面](https://private-user-images.githubusercontent.com/83439590/503101191-d59b86f2-a64b-431f-bdc4-8531de23d55c.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjA5NDMxMTIsIm5iZiI6MTc2MDk0MjgxMiwicGF0aCI6Ii84MzQzOTU5MC81MDMxMDExOTEtZDU5Yjg2ZjItYTY0Yi00MzFmLWJkYzQtODUzMWRlMjNkNTVjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEwMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMDIwVDA2NDY1MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTg5ODVlMmQ2NDFkZmMzM2M1Njc0NTM4Mzg1YTY1M2I2NTA3MTYyNTc4MDYwYWY3MDZhOGEyNzNlNDI5YjZhNmImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.qhitD0BTYC9w-cOBH0SuuKMqH8DhCyDQ2bKrN6qf5Os)

*个性化设置选项，关闭应用程序*

### 背景图自定义

![自定义背景图](https://private-user-images.githubusercontent.com/83439590/503101193-cf9327f2-c97c-4246-82f9-e3a31571dece.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NjA5NDMxMTIsIm5iZiI6MTc2MDk0MjgxMiwicGF0aCI6Ii84MzQzOTU5MC81MDMxMDExOTMtY2Y5MzI3ZjItYzk3Yy00MjQ2LTgyZjktZTNhMzE1NzFkZWNlLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTEwMjAlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUxMDIwVDA2NDY1MlomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWZiN2Q3NTc5OGZjNDY0NzgyZjRmYTU0NzcyYzNiMGFlZTVmZDJkNjY5OTg0NzJjMzg0ZmRlMjY4NDM3NmEyZDImWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.VbIx5iHW9nRKoeI9xv7WSkUsPSZRqsCN3mJMxt_orow)

## 🚀 下载安装

### 直接下载
从 [Releases](https://github.com/doubsumi/NotosIsland/releases) 页面下载最新的 `NotosIsland.exe` 文件。

### 使用步骤
1. 下载 `NotosIsland.exe`
2. 双击运行即可
3. 程序会自动在屏幕顶部居中显示
4. 双击悬浮窗切换显示模式

## 🛠️ 从源码运行

### 环境要求
- Python 3.6+
- Windows 10/11

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行程序
```bash
python main_v1.2.py
```

## 📦 依赖项

- PyQt5 - 图形界面
- psutil - 系统信息获取
- GPUtil - GPU信息获取
- pywin32 - Windows API调用

## 🔧 构建

使用PyInstaller打包为可执行文件：

```bash
pyinstaller -F main_v1.2.py
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如果遇到问题，可以通过以下方式联系：
- 提交 [Issue](https://github.com/doubsumi/NotosIsland/issues)

---

**NoteosIsland** - 让系统监控更简单直观 🎯

## 🙏 致谢

### 特别感谢

这是一次AI代码编写尝试，虽然本人的确是一名Python爱好者，但是本项目尝试在开发过程中完全使用AI工具生成全部代码，完成所有需求和解决所有问题，本人仅不断提出新需求，改进需求和抛出问题，今天的AI工具已经具备出色的，令人惊喜的专业性：

- **deepseek** - 核心开发贡献者
  - 负责了项目几乎所有的代码实现
  - 提供了完整的技术架构设计
  - 协助我解决了打包部署中出现的技术问题
  - 优化了用户界面和交互体验
  - 完成了这篇文档

- **[doubsumi]** - 项目发起人与产品经理
  - 提出项目核心创意和产品需求
  - 定义功能规格和用户体验
  - 负责项目管理和发布

### 技术致谢
感谢以下开源项目为本程序提供支持：
- PyQt5 - 图形界面框架
- psutil - 系统监控库
- GPUtil - GPU信息获取
- PyInstaller - 应用打包工具