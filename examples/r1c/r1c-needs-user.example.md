# R1C Needs-User Example

status: review-candidate example
canonical: no

```text
KDSL_RESULT:
SCHEMA:kdsl-r1c@0.1-draft
STATUS:needs_user
PHASE:Runtime UI confirmation
S:build/静的検証は完了したがtarget UIの実機確認が必要
FILES:["src/App/MainWindow.xaml"]
WHY:表示崩れの解消はbuild結果だけでは確認できず、対象Windows環境のruntime観測が必要なため
CMD:["dotnet build App.sln"]
VERIFY:{"pass":["dotnet build App.sln"],"fail":[],"not_run":["target Windows UI smoke"]}
RT:{"state":"u","basis":"U実機確認待ち"}
RISK:["runtime_unverified","build pass != RT:v"]
NEXT:{"proposal":"Uがtarget画面の表示と操作を確認し観測結果を共有","authority":"proposal_only"}
COMMIT:{"actual":null,"proposed":"UI: correct target layout","permission_basis":"none"}
```

Boundary notes:

```text
build pass != RT:v
RT:u→U実機確認待ち
NEXT→確認依頼であり次task自動実行許可ではない
COMMIT.proposed != commit authority
```
