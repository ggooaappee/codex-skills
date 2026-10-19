# GitHub 发布流程

## 前置检查

```powershell
gh auth status
gh repo view OWNER/REPO --json name,url,defaultBranchRef
```

不确定目标仓库时先问用户，不要猜测后推送。

## 安全边界

1. 仓库只放技能本体：`SKILL.md`、`agents/`、`references/`、`scripts/`、空白模板。
2. 不提交带学号、姓名、班级的成品报告、运行截图或作业压缩包。
3. 不提交课程课件原件（PPTX 等）和本机绝对路径。
4. 只增加或修改本次明确授权的内容，提交前看 `git diff --stat`。

## 发布

```powershell
git clone https://github.com/OWNER/REPO.git work/repo
# 复制技能目录到仓库根目录，更新 README 的技能列表
git -C work/repo add data-structure-labs README.md
git -C work/repo -c user.name="..." -c user.email="..." commit -m "Add data-structure-labs skill"
git -C work/repo push
```

推送后核对：

```powershell
git -C work/repo status --short
git -C work/repo log -1 --oneline
gh repo view OWNER/REPO --json pushedAt
```

认证或权限不足时保留本地提交，并说明阻塞原因。
