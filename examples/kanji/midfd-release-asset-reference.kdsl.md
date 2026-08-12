KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: dense
safety: normal
agent: required

局面: MidFD v2026.08.11 Asset差替/Portal同期

正本:
候補:=SHA `7cb5fe1dcd54cb5e70a4ddd02152d31cbfc2f2cc`/tag `v2026.08.11`/zip `C:\tmp\MidFD-ReleaseCandidate-v2026.08.11-7cb5fe1d-package\release\MidFD-win-x64.zip`/size `3,757,434`/hash `bfe23bf59be9119d49e31c4d681e6266b3b81ea126a3e70d9966b5c3500063ac`
公開:=main/tag `f8d837bbeeb3e100ed09f536383bc21272dd929b`/Release `v2026.08.11`/旧Asset hash `c87c26fa2ad1c8a6a5b3902989453bf36ed3346960d27a2cd86f1c795f567800`
配布:=Asset/remote/live=候補
保全:=公開不変/他Asset・対象外dirty不変/候補再生成×

目的:
GitHub CLI→既存Assetを候補へ置換→remote一致後Portal必要差分同期→live一致

成功条件:
配布/保全/Portal同期完

承認境界:
Asset置換/Release必要更新/Portal更新=U済;再承認×

作業:
1. 候補/公開/dirty基線照合
2. `gh --version`/`gh auth status`→CLI成立;不可→停止
3. `gh release upload --help`→同名安全置換可確認;不可→停止
4. `gh release upload`使用; 引数:=候補tag/候補zip; option:=`--clobber`; 他Asset/Release再作成×
5. remote再取得→配布(remote)照合;不一致→停止
6. Portal依存箇所特定→必要差分のみdev/public同期→通常push
7. live新規取得→配布(live)照合→公開/Portal最終照合

検証:
local→remote→live size/hash連鎖一致/公開pre-post一致/Portal HEAD-origin一致

保持:
Bytes=`#,##0 B`/Settings補正/`HumanReadable`/`KB/MB`/Markdown/ZIP/Command/Mark/縦tab/README契約/保全

禁止:
browser/file chooser/候補再生成/dev source編集/public source同期/public main操作/tag操作/Release再作成/他Asset変更/package加工/Portal全面再構築/amend/rebase/merge/reset/force push

停止条件:
gh不可/候補不一致/公開不一致/CLI安全置換不可/remote不一致/他Asset変更要/対象外semantic変更要/live不一致

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
