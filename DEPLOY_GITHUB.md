# 部署到 GitHub Pages（免费托管，push 即可用）

本项目用 GitHub Actions 每天自动抓两次热点（北京 09:00 / 21:00），抓完自动更新并发布到 GitHub Pages，**完全免费**。全程约 15 分钟。

---

## 前置：注册 GitHub 账号
打开 https://github.com/ ，点 Sign up 注册（邮箱 + 密码即可）。

> 仓库建议选 **Public（公开）**——GitHub Pages 免费版只对 Public 仓库开放；Private 仓库需要 Pro（$4/月）。内容本身就是公开热点数据，不含密钥（密钥放 Secrets，不进代码）。

---

## 第一步：新建仓库
1. 登录后右上角 **+ → New repository**。
2. Repository name 填：`hotspot-radar`（或你喜欢的名字，记住它，访问地址会用到）。
3. 选 **Public**。
4. 不要勾选 "Add a README"（避免冲突），点 **Create repository**。

---

## 第二步：上传代码（二选一）

### 方式 A：网页直接上传（最简单，不用装工具）
1. 在刚建的仓库页点 **uploading an existing file**。
2. 把整个 `hotspot-radar-cloud` 文件夹里的**所有内容**（不是文件夹本身）拖进去：
   - `adapters/`、`site/`、`manual/`、`.github/`、`requirements.txt`、`run_daily.py`、`scoring.py`、`.gitignore`
   - **注意**：`.github` 是隐藏文件夹，Windows 地址栏直接输入路径拖入；上传后网页上能看到 `.github/workflows/daily.yml` 才算对。
3. 点底部 **Commit changes**。

### 方式 B：命令行（适合装了 git 的同学）
```bash
cd hotspot-radar-cloud
git init
git add .
git commit -m "init"
# 把下面的 URL 换成你刚建的仓库地址
git remote add origin https://github.com/你的用户名/hotspot-radar.git
git branch -M main
git push -u origin main
```

### 方式 C：本机有 gh CLI 一键建仓（可选）
```bash
gh auth login          # 按提示浏览器登录
gh repo create hotspot-radar --public --source=. --push
```

---

## 第三步：开启 GitHub Pages
1. 仓库页 **Settings → 左侧 Pages**。
2. **Build and deployment → Source** 选 **GitHub Actions**（不要选 Deploy from a branch）。
3. 完成。

---

## 第四步：手动跑一次验证
1. 仓库页 **Actions** 标签。
2. 左侧选 **Daily Hotspot** workflow。
3. 右侧 **Run workflow → Run workflow**。
4. 等 1-2 分钟变绿勾。
5. 访问你的站点：`https://你的用户名.github.io/hotspot-radar/`
   （仓库名是啥就是啥；若 404 等 30 秒再刷，Pages 首次部署要等一会）。

之后每天 9 点 / 21 点（北京时间）自动跑，无需手动。

---

## 第五步：（可选）接入付费平台 Key
当前免费源已能跑：Google News RSS（四语种）+ 百度热搜 + YouTube 频道 RSS + 节日日历。
要接 TikTok / Meta / Amazon / Shopee 等付费平台，**加 Key 无需改代码，次日自动生效**：

1. 仓库 **Settings → Secrets and variables → Actions → New repository secret**。
2. 按下表逐个加 Name（左边）和 Value（右边申请）：

| 平台 | Secret 名称 | 申请入口 |
|---|---|---|
| TikTok 开放平台 | `TIKTOK_CLIENT_KEY`、`TIKTOK_CLIENT_SECRET` | https://developers.tiktok.com/ |
| Meta (IG/FB) | `META_ACCESS_TOKEN` | https://developers.facebook.com/ |
| Amazon PA-API | `AMAZON_PA_ACCESS_KEY`、`AMAZON_PA_SECRET_KEY` | https://affiliate-program.amazon.gov/ |
| EchoTik (TikTok 数据) | `ECHOTIK_API_KEY` | https://www.echotik.live/ |
| FastMoss (TikTok 数据) | `FASTMOSS_API_KEY` | https://www.fastmoss.com/ |
| Shopee 开放平台 | `SHOPEE_API_KEY`、`SHOPEE_API_SECRET` | https://open.shopee.com/ |
| YouTube Data API | `YOUTUBE_API_KEY` | https://console.cloud.google.com/ |

加完后去 Actions 手动 Run 一次，或等次日自动跑。

---

## 本地/国内网络注意
- Google News RSS 在国内网络可能超时——**这正常**，Actions 在海外服务器跑不受影响。
- 微博/知乎/抖音聚合海外 IP 被墙，默认关闭；国内本地调试时设环境变量 `ENABLE_DOMESTIC=1` 再跑。
- 本地运行：`pip install -r requirements.txt` 后 `python run_daily.py`，结果在 `site/data/`。

---

## 限制说明
- GitHub Pages 对 Public 仓库免费；Actions 免费额度 **2000 分钟/月**，本任务每次约 2-3 分钟、每天 2 次 ≈ 180 分钟/月，够用。
- 定时任务在 GitHub 可能**延迟数分钟到十几分钟**，非精确触发。
- Pages 站点内容公开，**密钥绝不放仓库**，只放 Secrets。
- 仅用官方 RSS/API，只抓摘要并回链原文，遵守平台条款。
