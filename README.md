# Lelyetia 知识库

使用 **MkDocs + Material for MkDocs** 搭建的个人知识库，涵盖深度学习、计算机视觉、医学图像、实用工具与科研工具。笔记位于 `docs/`，网站配置位于 `mkdocs.yml`。

## 首次启动

先安装 Python 3（需包含 `pip` 和 `venv`），然后在终端进入本仓库根目录，也就是包含 `mkdocs.yml` 的目录。

### Linux / macOS

```bash
cd /你的路径/Lelyetia-knowledge
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m mkdocs serve
```

### Windows（PowerShell）

```powershell
cd C:\你的路径\Lelyetia-knowledge
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m mkdocs serve
```

启动后，在浏览器打开 **<http://127.0.0.1:8000/lelyetia-knowledge/>**，具体地址以终端的 `Serving on` 输出为准。修改并保存 `docs/` 下的笔记后，预览页面会自动刷新。终端需保持运行，按 **Ctrl+C** 停止服务。

如果 Windows 阻止执行激活脚本，可以直接用虚拟环境中的 Python：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m mkdocs serve
```

## 以后每次启动

依赖安装过后，只需进入仓库、激活虚拟环境并启动：

```bash
cd /你的路径/Lelyetia-knowledge
source .venv/bin/activate
python -m mkdocs serve
```

Windows 将激活命令替换为 `.\.venv\Scripts\Activate.ps1`，也可直接运行 `.\.venv\Scripts\python.exe -m mkdocs serve`。

只有新建环境或更新 `requirements.txt` 后，才需要重新执行 `python -m pip install -r requirements.txt`。

## 添加和修改笔记

```text
Lelyetia-knowledge/
├── README.md             # 启动与维护说明
├── requirements.txt      # Python 依赖
├── mkdocs.yml            # 网站名称、主题、导航和扩展配置
└── docs/
    ├── main_page.md      # 知识库介绍与首页正文
    ├── index.html        # 根目录入口，自动跳转至介绍页
    ├── deep-learning/    # 深度学习
    ├── computer-vision/  # 计算机视觉
    ├── medical-imaging/  # 医学图像
    ├── practical-tools/  # 实用工具
    ├── research-tools/   # 科研工具
    ├── learning-resources/ # 按学科归类的学习资源与课程笔记
    ├── assets/           # 图片等静态资源
    └── javascripts/      # MathJax 数学公式配置
```

- 修改首页：编辑 `docs/main_page.md`。
- 添加笔记：在 `docs/` 对应目录下创建 Markdown 文件。
- 添加导航：在 `mkdocs.yml` 的 `nav` 中加入新页面，路径相对于 `docs/`。例如 `practical-tools/example.md`。
- 图片等资源放在 `docs/assets/`，在笔记中使用相对路径引用。

导航路径相对于 `docs/`，不需要再写 `docs/` 前缀。分类使用英文冒号和空格，下面的页面缩进对齐，例如：

```yaml
- 计算机科学基础:
    - 分类总览: learning-resources/fundamentals-of-computer/index.md
    - CS50x: learning-resources/fundamentals-of-computer/CS50x.md
```

### 文内引用与参考资料

已启用 Markdown 脚注及悬停预览，无需安装额外的引用插件。正文中使用 `[^标识符]`，在文末统一写来源：

```markdown
这里是根据课程整理的内容。[^cs50]
同一来源可以再次引用。[^cs50]

## 参考资料

[^cs50]: Harvard University. [CS50x](https://cs50.harvard.edu/x/) [在线课程]. 访问日期：2026-11-03。
```

页面会显示上标 `[1]`，悬停或聚焦可查看来源，点击可跳到文末；文末的返回箭头可回到引用处。同一标识符复用同一个编号。编号按文末定义的顺序生成，建议按正文首次引用的顺序排列定义。

网页记录作者或机构、标题、链接与访问日期；书籍补充版本、章节或页码，论文补充 DOI 或公开链接。逐字摘录可放入 `>` 引用块并附来源，转述则在对应句子或段落末尾标注。可复用 `templates/note-with-references.md`，现有示例位于 `docs/learning-resources/fundamentals-of-computer/CS50x.md`。

### 笔记版本与更新记录

每篇笔记的文末保留一个“版本记录”表格，记录版本号、更新日期和更新概述。网站会自动读取其中的最新版本，在笔记标题下显示当前版本和最后更新日期，无需另外维护页首信息。

```markdown
## 版本记录 {#version-history}

| 版本号 | 更新日期 | 更新概述 |
| --- | --- | --- |
| v0.2.0 | 2026-11-03 | 补充示例并修正术语。 |
| v0.1.0 | 2026-11-03 | 建立笔记。 |
```

更新笔记后，在表格最上方新增一行，保留旧记录。版本号使用 `v主版本.次版本.修订号`，例如 `v0.1.1`、`v0.2.0`、`v1.0.0`；系统按三个数字比较版本，新版本的日期不得早于旧版本。同一天可以更新多个版本。表格放在正文与参考资料之后，概述中的竖线写成 `\|`。

版本记录自 2026-11-03 启用，各篇笔记按自己的版本表格维护；此前未记录的修改不作追溯。新笔记可以复制 `templates/note.md`，需要引用的笔记使用 `templates/note-with-references.md`，并将模板中的 `YYYY-MM-DD` 替换为实际日期。缺失记录、无效日期、重复版本号或缺少概述会在构建时提示具体文件与原因。

### 代码块样式

所有代码块统一使用左上角红、黄、绿三个圆点的窗口样式，并支持语法高亮和复制按钮。继续使用普通围栏代码块即可，也可填写文件名：

````markdown
```python title="example.py"
print("Hello, world!")
```
````

首次启用版本功能后，重新启动一次 `python -m mkdocs serve`。以后修改笔记及其版本表格会自动刷新；修改 `hooks/note_versions.py` 后也需重新启动预览服务。

## 构建静态网站

在已激活虚拟环境的仓库根目录运行：

```bash
python -m mkdocs build
```

生成的网站位于 `site/`，可用于静态网站部署。`site/` 和本地虚拟环境 `.venv/` 已加入 Git 忽略列表。

版本规则的自动检查可运行 `python -m unittest discover -s tests`，完整检查可运行 `python -m mkdocs build --strict`。

`mkdocs.yml` 中的 `site_url` 用于配置网站正式地址，本地预览仍使用终端输出的地址。当前仓库没有自动部署工作流；本地启动和构建都不需要先配置部署。

## 常见问题

| 情况 | 处理方法 |
| --- | --- |
| 提示 `No module named mkdocs` 或缺少 `material` 主题 | 确认已激活 `.venv`，然后执行 `python -m pip install -r requirements.txt`。 |
| 提示找不到 `mkdocs.yml` | 先进入仓库根目录，再运行启动命令。 |
| 默认端口被占用 | 使用 `python -m mkdocs serve -a 127.0.0.1:8001`，然后访问 <http://127.0.0.1:8001/lelyetia-knowledge/>。 |
| Linux 创建虚拟环境时提示缺少 `venv` 或 `ensurepip` | 安装系统对应的 Python venv 软件包后重试，例如 Ubuntu / Debian 的 `python3-venv`。 |
| 数学公式没有渲染 | 当前配置从 `unpkg.com` 加载 MathJax，检查浏览器能否访问该地址。 |

退出虚拟环境可运行 `deactivate`。
