# Amazon Ops AI Agent

面向亚马逊运营场景的 AI Agent，用于 Listing 优化、广告报表分析、买家邮件回复和产品图片方案生成。

## 功能

- Listing 优化：生成标题、五点描述、产品描述、Search Terms 和图片卖点方案。
- 广告报表分析：根据 CTR、CPC、Spend、Sales、ACOS、ROAS、Orders 等指标识别高花费低转化词、低 ACOS 优质词、需要否定的关键词和预算调整建议。
- 买家邮件回复：按售后场景生成符合亚马逊沟通规范的英文回复。
- 图片方案生成：输出主图、场景图、卖点图、尺寸图、对比图等拍摄/设计 brief。
- 结构化输出：AI 结果以 JSON 为主，便于复核和二次加工。

## 快速开始

```powershell
cd D:\新建文件夹\amazon_ops_agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

配置 OpenAI API Key：

```powershell
$env:OPENAI_API_KEY="你的 API Key"
```

广告报表分析可以不依赖 API Key：

```powershell
amazon-agent ads --report examples/sample_ads_report.csv --out output/ads_analysis.json
```

Listing 优化：

```powershell
amazon-agent listing --asin B0TEST123 --product examples/product_brief.json --out output/listing_plan.json
```

买家邮件回复：

```powershell
amazon-agent email --scenario refund_request --message "The item arrived damaged. I want a refund." --out output/email_reply.json
```

图片方案生成：

```powershell
amazon-agent images --product examples/product_brief.json --out output/image_plan.json
```

## 广告报表字段

脚本会自动兼容常见字段名。建议报表至少包含：

- Campaign
- Ad Group
- Customer Search Term 或 Keyword
- Impressions
- Clicks
- Spend
- Sales
- Orders

可选字段：

- CTR
- CPC
- ACOS
- ROAS

如果可选字段缺失，系统会自动计算。

## GitHub 上传

当前运行环境没有检测到 `git` 和 GitHub CLI (`gh`) 命令，所以我无法在本机直接完成上传。安装 Git 后可以执行：

```powershell
cd D:\新建文件夹\amazon_ops_agent
git init
git add .
git commit -m "Initial Amazon ops AI agent"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

也可以在 GitHub 网页端新建仓库后，把本目录中的文件上传。

