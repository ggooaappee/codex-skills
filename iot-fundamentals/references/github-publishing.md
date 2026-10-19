# GitHub 发布流程

## 前置检查

```bash
gh auth status
gh repo view OWNER/REPO --json name,url,defaultBranchRef
```

如果不确定目标仓库，先向用户确认，不要推测后推送。

## 安全更新

1. 克隆目标仓库到工作区。
2. 检查 `git status` 和现有目录，避免覆盖同名 skill。
3. 只增加或修改本次明确授权的内容。
4. 不提交 `.pptx` 课件原件、个人学号、姓名、访问 token 或调试截图中的隐私信息。
5. 不把本机绝对路径或用户目录结构写进公共仓库文档。
6. 提交前查看 `git diff --stat` 和关键文件 diff。

## 发布

```bash
git add <具体文件>
git commit -m "<清楚的提交说明>"
git push
```

推送后检查：

```bash
git status --short
git log -1 --oneline
gh repo view OWNER/REPO --json pushedAt
```

如果认证、权限或远端状态阻止推送，保留本地提交并清楚报告阻塞原因。
