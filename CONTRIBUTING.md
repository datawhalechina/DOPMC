# Datawhale 社区贡献手册
本贡献指南是 Datawhale 与其下属开源项目团队所约定的协议，由[ Datawhale 开源项目管理委员会（Datawhale Open-source Project Management Committee，简称DOPMC）](https://github.com/datawhalechina/DOPMC)制定并发行，其旨在规范化管理开源项目，明确 Datawhale 和开源项目团队各自的责任与义务。

### 1. 行为规范
- 每个开源项目主体负责人原则上有且只能有一位；
- 我们鼓励开放的沟通方式，Issue 和 Github Discussion 是项目负责团队进行沟通并与社区成员交流的最关键渠道，项目负责团队要公开的讨论项目相关信息，如项目规划，项目进展，并将对应的 Roadmap 更新到项目主页；
- 项目负责团队要及时公开的参与到 Issue 与 Github Discussion 中去；
- 组织项目并不完全归属于项目负责团队，因此项目在对外产生合作时，须由 DOMPC 成员辅助项目负责人共同对接；
- 项目产生的商业收益大部分归属于项目负责团队及 Datawhale 社区共同所有。


### 2. 开源项目管理流程
Datawhale 社区开源项目会经历五个流程，如下图所示：
![Datawhale 开源项目管理流程](https://tva1.sinaimg.cn/large/e6c9d24ely1h1xra9vrsjj230e0lewjk.jpg)

### 2.1 立项规范
0. 项目负责人阅读熟知并同意《Datawhale 社区贡献手册》中的所有内容；
1. 首先需要在 [DOPMC](https://github.com/datawhalechina/DOPMC) 项目的中创建 ISSUE 进行初步讨论，打开[创建 ISSUE](https://github.com/datawhalechina/DOPMC/issues/new/choose) 页面后点击立项按钮，根据模板填写项目的相关信息，提交的 ISSUE 会随机分配给三分之一的 [DOPMC 成员](./ROLES.md)；
2. 在 ISSUE 创建的两周内，[DOPMC 成员](./ROLES.md)会公开讨论该立项是否符合 Datawhale 社区贡献手册，并会在 ISSUE 下通过评论进行投票，同意会评论 `/LGTM`，否则需要提出相应意见或建议；
3. 若投同意票人数超过 DOMPC 成员的三分之一则该项目达到立项标准，DOPMC 成员会将其移动到 [Datawhale Project](https://github.com/datawhalechina/DOPMC/projects/1?fullscreen=true) 看板对应的筹划阶段；
4. 立项成功后 DOPMC 成员会在 Datawhale 官方 GitHub Organization 下为其创建 Team 和 Repository；
5. 若没有得到 DOPMC 成员半数投票，则需要修改相应的立项信息或终结立项。

### 2.2 内容规范
- 文档类的项目统一采用 Docsify/Sphinx 进行在线展示，同时也需要在项目完成后同步发行 PDF 版本（推荐使用 LaTeX 进行排版）；
- 项目根目录下的README.md里必须包含以下内容（模板参见附录）：
  - 项目负责人以及负责团队的联系方式；
  - 项目贡献者的名单；
  - Datawhale 的外宣信息；
  - 项目所采用的开源协议；
  - 若非完全原创内容，则需要给出必要的版权说明；
- 项目负责人需要为其负责的项目撰写一份《贡献指南》，供其他贡献者使用；

### 2.3 协作规范
- 贡献者必须严格按照项目负责人撰写的《贡献指南》发起 Pull Request；
- 贡献者在提交 Pull requests 后需要项目负责团队对其进行 Review；

## 附录
### 项目 README.md模板
[README_example.md](https://github.com/datawhalechina/DOPMC/blob/df4965d7eb6488fd2b33153b1143006f30c81a6e/README_example.md)

### 相关教程
- Sphinx 使用教程（by 耿远昊）：https://www.bilibili.com/video/BV12B4y1u7PF