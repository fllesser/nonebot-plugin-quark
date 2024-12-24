<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-quark/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-quark/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-quark

_✨ 夸克云盘资源搜索 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fllesser/nonebot-plugin-quark.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-quark">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-quark.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

</details>

> [!NOTE]
> 模板库中自带了一个发布工作流, 你可以使用此工作流自动发布你的插件到 pypi

<details>
<summary>配置发布工作流</summary>

1. 前往 https://pypi.org/manage/account/#api-tokens 并创建一个新的 API 令牌。创建成功后不要关闭页面，不然你将无法再次查看此令牌。
2. 在单独的浏览器选项卡或窗口中，打开 [Actions secrets and variables](./settings/secrets/actions) 页面。你也可以在 Settings - Secrets and variables - Actions 中找到此页面。
3. 点击 New repository secret 按钮，创建一个名为 `PYPI_API_TOKEN` 的新令牌，并从第一步复制粘贴令牌。

</details>

> [!IMPORTANT]
> 这个发布工作流需要 pyproject.toml 文件, 并且只支持 [PEP 621](https://peps.python.org/pep-0621/) 标准的 pyproject.toml 文件

<details>
<summary>触发发布工作流</summary>
从本地推送任意 tag 即可触发。

创建 tag:

    git tag <tag_name>

推送本地所有 tag:

    git push origin --tags

</details>

## 📖 介绍

这里是插件的详细介绍部分

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
<details>
<summary>conda</summary>

    conda install nonebot-plugin-quark
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_quark"]

</details>


## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|

| qs | 群员 | 否 | - | 搜索 |


