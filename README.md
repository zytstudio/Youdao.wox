# 有道翻译

**需要填写`app_key`与`app_secret`**

**需要填写`app_key`与`app_secret`**

**需要填写`app_key`与`app_secret`**

## 配置步骤 

1. 在Wox中安装此插件

   ```
   wpm install 有道翻译
   ```

2. 转到[有道智云AI开放平台](https://ai.youdao.com/)，创建一个账号，然后创建一个应用

3. 设置中找到此插件，点击“打开目录”

4. 在插件目录中将`key.example.ini`重命名为`key.ini`

5. 用记事本打开`key.ini`，将其中的`app_key`的值替换成应用ID，`app_secret`的值替换成应用密钥

6. 保存文件，测试翻译功能是否正常

## 注意事项

由于框架限制，每次输入框更改都会触发一次API调用，次数过多会触发错误，更新一次输入框即可刷新。目前没有什么好的修复方法，建议使用拼音输入法输入，输入完切换成英文。

# Youdao.wox

A wox plugin using youdao api to translate input text. Python implement version from [Wox.Plugin.Youdao](https://github.com/qianlifeng/Wox.Plugin.Youdao), adding proxy support.

