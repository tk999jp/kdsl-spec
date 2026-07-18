KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal

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

対象:
`MainForm.cs`／`MainForm.FileOperations.cs`／`Services/FileOperationService.cs`／関連test

非対象:
helper／IPC／manifest／security再設計
新framework
追加hardening

作業:
active caller確認→順序補正→src cleanup→状態反映→targeted test→Release build→full test

検証:
`dotnet build MidFD.csproj -c Release --no-restore`
full `MidFD.Tests`
`git diff --check`

停止条件:
既存user-visible merge契約変更が不可避／baseline破棄必須

報告:
簡潔KDSL_RESULT
