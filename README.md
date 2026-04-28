# Amazon 广告与 Listing 运营助手

这是一个给亚马逊日常运营使用的小工具，主要解决几个重复度比较高的工作：广告报表筛选、Listing 文案整理、买家邮件回复和产品图片方案梳理。

项目最初是围绕实际运营流程做的。平时一个 ASIN 会涉及关键词、广告花费、转化、Search Term、竞品卖点和买家消息等信息，如果全部手动看表和整理，效率比较低，也容易因为不同人判断标准不一致导致结论不稳定。这个工具把常规判断规则先固化下来，再把需要生成文案或方案的部分交给模型处理，最后输出可复核、可直接执行的建议。

## 主要功能

### 广告报表分析

支持 CSV / Excel 广告报表，自动计算或读取以下指标：

- CTR
- CPC
- Spend
- Sales
- ACOS
- ROAS
- Orders

目前会重点筛出几类数据：

- 花费高但转化差的搜索词
- ACOS 较低、值得加预算或单独拉 exact 的关键词
- 有花费但无订单的否定词候选
- ROAS 表现较好的预算调整候选

广告分析模块不依赖 API Key，可以直接离线跑。

### Listing 优化

根据产品信息、关键词和竞品备注生成：

- Title
- Bullet Points
- Product Description
- Search Terms
- 图片卖点方向
- 合规注意点

### 买家邮件回复

根据售后场景和买家原文生成英文回复，重点控制语气、平台规范和下一步处理动作，避免出现索评、站外联系、补偿换好评等风险表达。

### 图片方案

根据产品卖点生成主图、场景图、功能图、尺寸图、对比图等方向的 brief，方便后续给设计或摄影沟通。

## 技术栈

- Python
- pandas
- OpenAI API
- Pydantic
- Prompt Engineering
- JSON 结构化输出

## 安装

```powershell
git clone https://github.com/Hector-xue/amazon.git
cd amazon
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

如果要使用 Listing、邮件和图片方案生成功能，需要配置 OpenAI API Key：

```powershell
$env:OPENAI_API_KEY="your_api_key"
```

也可以复制 `.env.example` 为 `.env` 后填写：

```text
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4.1-mini
```

## 使用示例

分析广告报表：

```powershell
amazon-agent ads --report examples/sample_ads_report.csv --out output/ads_analysis.json
```

生成 Listing 优化方案：

```powershell
amazon-agent listing --asin B0TEST123 --product examples/product_brief.json --out output/listing_plan.json
```

生成买家邮件回复：

```powershell
amazon-agent email --scenario refund_request --message "The item arrived damaged. I want a refund." --out output/email_reply.json
```

生成图片方案：

```powershell
amazon-agent images --product examples/product_brief.json --out output/image_plan.json
```

## 广告报表字段

建议报表至少包含这些字段：

- Campaign
- Ad Group
- Customer Search Term 或 Keyword
- Impressions
- Clicks
- Spend
- Sales
- Orders

字段名称不完全一致也可以，程序会兼容一部分常见命名，比如 `Campaign Name`、`Cost`、`7 Day Total Sales` 等。

## 项目结构

```text
amazon_ops_agent/
├─ examples/                 # 示例产品信息和广告报表
├─ scripts/                  # 本地运行和上传脚本
├─ src/amazon_ops_agent/
│  ├─ ads_analysis.py        # 广告报表清洗与分类
│  ├─ ai_client.py           # OpenAI 调用封装
│  ├─ cli.py                 # 命令行入口
│  ├─ listing.py             # Listing 优化
│  ├─ email_reply.py         # 买家邮件回复
│  ├─ image_plan.py          # 图片方案生成
│  └─ schemas.py             # 输出结构定义
└─ tests/
```

## 当前状态

这个项目目前偏向内部运营工具，核心逻辑已经可以跑通。后续计划继续补：

- 更细的广告活动层级分析
- 不同类目的 Listing 模板
- 批量 ASIN 处理
- 简单 Web 界面
- 更多报表格式兼容

