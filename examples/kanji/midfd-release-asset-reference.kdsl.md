KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: dense
safety: normal
agent: required

局面: MidFD v2026.08.11 Asset修正版差替/CLI

正本:
候補:=SHA `7cb5fe1dcd54cb5e70a4ddd02152d31cbfc2f2cc`/tag `v2026.08.11`/PV `v2026.08.11+7cb5fe1dcd54cb5e70a4ddd02152d31cbfc2f2cc`/zip `C:\tmp\MidFD-ReleaseCandidate-v2026.08.11-7cb5fe1d-package\release\MidFD-win-x64.zip`/size `3,757,434`/hash `bfe23bf59be9119d49e31c4d681e6266b3b81ea126a3e70d9966b5c3500063ac`
公開:=main/tag `f8d837bbeeb3e100ed09f536383bc21272dd929b`/Release `v2026.08.11`/旧Asset size `3,757,465`/hash `c87c26fa2ad1c8a6a5b3902989453bf36ed3346960d27a2cd86f1c795f567800`
dev:=HEAD/origin `7cb5fe1dcd54cb5e70a4ddd02152d31cbfc2f2cc`

目的:
browser/file chooser×
GitHub CLI→既存Assetを候補へ置換
remote再取得=候補→Portal同期→再公開

成功条件:
公開main/tag不変
Release維持/対象Assetのみ候補化
remote/live=候補
Portal同期完

承認境界:
Asset置換/Release必要更新/Portal更新=U済;再承認×

作業:
1. 候補/公開/dev/dirty基線照合
2. `gh --version`/`gh auth status`/repo認証;不成立→停止;browser代替×
3. `gh release upload --help`→同名安全置換可確認;不可→停止
4. 正本zipのみ置換;他Asset/Release/tag変更×
5. Release metadata照合→remote再取得→size/hash=候補;不一致→停止
6. 公開main/tag再照合;追加操作×
7. Portal dev/public基線固定→Release依存値のみ更新
8. dev検証→必要差分commit/push
9. public同期→不要管理物混入×→必要差分commit/push
10. Pages/live検証→download=候補

検証:
local→remote→live size/hash連鎖一致
GitHub/Portal各HEAD-origin一致

保持:
Bytes=`#,##0 B`/Settings補正/`HumanReadable`/`KB/MB`/Markdown/ZIP/Command/Mark/縦tab/README契約
候補/公開/他Asset/対象外dirty不変

禁止:
候補再生成/dev source編集/public source同期/public main操作/tag操作/Release再作成/他Asset変更/package加工/Portal全面再構築/amend/rebase/merge/reset/force push

停止条件:
gh不可/候補不一致/公開基線不一致/CLI安全置換不可/remote不一致/他Asset変更要/対象外repo状態変化/live不一致

報告: R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: CLI確認/Asset置換/remote検証/Portal同期/live検証
検証: 未実行
実機: 未確認
次: CLI確認
停止理由: なし
