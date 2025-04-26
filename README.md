<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-quark ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fllesser/nonebot-plugin-quark.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-quark">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-quark.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>



## 📖 介绍

夸克云盘搜索插件

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-quark --upgrade

使用官方源更新，常用于刚发版，其他源未同步的时候

    nb plugin install nonebot-plugin-quark --upgrade -i https://pypi.org/simple

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>conda</summary>

    uv add nonebot-plugin-quark
</details>
<details>
<summary>pip</summary>

    pip install nonebot-plugin-quark --upgrade -i https://pypi.org/simple
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-quark
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-quark
</details>


打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_quark"]

</details>


## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| qs | 群员 | 否 | - | 搜索 |


