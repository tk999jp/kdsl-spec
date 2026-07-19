KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal
agent: required

局面:
MidFD跨volume nested-link移動補正

目的:
通常dir配下symlink／junctionを跨volume move／cut-paste／mergeで正しく移動

成功条件:
- helper先行dst親作成済→collision失敗禁止
- 通常内容→既存copy／merge
- helper成功link→src link objectのみ削除
- failed／unsupported／UAC取消→src保持
- src dir空時のみ削除
- partial→mark／clipboard保持

根拠:
再現事象／関連code／test

正本:
`G:\source\repos\MidFD`／`main`／baseline確認

権限:
読取／編集／試験=可、commit／push=承認待

承認境界:
commit／push直前

対象:
`MainForm.cs`／`MainForm.FileOperations.cs`／`Services/FileOperationService.cs`／関連test

非対象:
helper／IPC／manifest／security再設計
新framework
追加hardening

作業:
active caller確認→順序補正→src cleanup→状態反映→targeted test→Release build→full test→結果確認

試験:
関連targeted test／Release build／full `MidFD.Tests`

検証:
`dotnet build MidFD.csproj -c Release --no-restore`
full `MidFD.Tests`
`git diff --check`

停止条件:
既存user-visible merge契約変更が不可避／baseline破棄必須

報告:
R1

K1:
状態: 計画
現在: 初期化
完了: なし
未完: active caller確認／順序補正／src cleanup／状態反映／targeted test／Release build／full test／結果確認
検証: 未実行
実機: 未確認
次: active caller確認
停止理由: なし
