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

启动后，在浏览器打开 **<http://127.0.0.1:8000/>**。修改并保存 `docs/` 下的笔记后，预览页面会自动刷新。终端需保持运行，按 **Ctrl+C** 停止服务。

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
    ├── index.md          # 网站首页
    ├── deep-learning/    # 深度学习
    ├── computer-vision/  # 计算机视觉
    ├── medical-imaging/  # 医学图像
    ├── practical-tools/  # 实用工具
    ├── research-tools/   # 科研工具
    ├── assets/           # 图片等静态资源
    └── javascripts/      # MathJax 数学公式配置
```

- 修改首页：编辑 `docs/index.md`。
- 添加笔记：在 `docs/` 对应目录下创建 Markdown 文件。
- 添加导航：在 `mkdocs.yml` 的 `nav` 中加入新页面，路径相对于 `docs/`。例如 `practical-tools/example.md`。
- 图片等资源放在 `docs/assets/`，在笔记中使用相对路径引用。

## 构建静态网站

在已激活虚拟环境的仓库根目录运行：

```bash
python -m mkdocs build
```

生成的网站位于 `site/`，可用于静态网站部署。`site/` 和本地虚拟环境 `.venv/` 已加入 Git 忽略列表。

`mkdocs.yml` 中的 `site_url` 用于配置网站正式地址，本地预览仍使用终端输出的地址。当前仓库没有自动部署工作流；本地启动和构建都不需要先配置部署。

## 常见问题

| 情况 | 处理方法 |
| --- | --- |
| 提示 `No module named mkdocs` 或缺少 `material` 主题 | 确认已激活 `.venv`，然后执行 `python -m pip install -r requirements.txt`。 |
| 提示找不到 `mkdocs.yml` | 先进入仓库根目录，再运行启动命令。 |
| 默认端口被占用 | 使用 `python -m mkdocs serve -a 127.0.0.1:8001`，然后访问 <http://127.0.0.1:8001/>。 |
| Linux 创建虚拟环境时提示缺少 `venv` 或 `ensurepip` | 安装系统对应的 Python venv 软件包后重试，例如 Ubuntu / Debian 的 `python3-venv`。 |
| 数学公式没有渲染 | 当前配置从 `unpkg.com` 加载 MathJax，检查浏览器能否访问该地址。 |

退出虚拟环境可运行 `deactivate`。
