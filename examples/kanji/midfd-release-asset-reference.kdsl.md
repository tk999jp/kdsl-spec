KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: dense
safety: normal
agent: required

局面: MidFD v2026.08.11 Asset差替/Portal同期

正本:
候補:=Tag `v2026.08.11`/Asset `MidFD-win-x64.zip`/Package `C:\tmp\MidFD-ReleaseCandidate-v2026.08.11-7cb5fe1d-package\release\MidFD-win-x64.zip`/size `3,757,434`/hash `bfe23bf59be9119d49e31c4d681e6266b3b81ea126a3e70d9966b5c3500063ac`
公開:=main `f8d837bbeeb3e100ed09f536383bc21272dd929b`/tag→`f8d837bbeeb3e100ed09f536383bc21272dd929b`
旧:=Asset hash `c87c26fa2ad1c8a6a5b3902989453bf36ed3346960d27a2cd86f1c795f567800`
保全:=Release/他Asset/source/design/開始dirty不変/候補再生成×

目的:
GitHub CLI→Assetのみ候補化→remote=候補→Portal必要差分同期→live=候補

成功条件:
remote/live=候補/公開・保全不変/Portal同期完

承認境界:
Asset置換/Release必要更新/Portal更新=U済;再承認×

作業:
1. 候補/公開/旧/保全基線照合
2. `gh --version`/`gh auth status`/`gh release upload --help`→CLI同名置換可;不可→停止
3. `gh release upload`使用; 引数:=候補Tag/Asset/Package; option:=`--clobber`; 保全変更×
4. remote再取得→候補照合;不一致→停止
5. Portal依存箇所→必要差分のみdev/public同期→通常push
6. live新規取得→候補照合→公開/保全最終照合

検証:
開始→remote→Portal→live→終了照合

禁止:
browser/file chooser/候補再生成/MidFD public操作/tag操作/Release再作成/他Asset変更/package加工/Portal全面再構築/amend/rebase/merge/reset/force push

停止条件:
gh不可/候補・公開・保全不成立/CLI安全置換不可/対象外semantic変更要

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
