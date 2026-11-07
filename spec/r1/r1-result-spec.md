# R1 — KDSL_RESULT最小報告

```text
KDSL_RESULT:
状態:
局面:
要約:
変更:
理由:
実行:
検証:
実機:
危険:
次:
commit:
```

状態は`成功／一部／停止／変更なし／失敗／U確認待`等、事実に応じて記載。未使用欄は受領側仕様に合わせ省略可。ただし取り込み側の必須欄は保持する。

```text
実行:=実際に実行したcommandのみ
検証:=実際に行った試験／結果のみ
未実行→成功扱禁止
build／lint／test／CI pass != RT:v
RT:v:=対象環境runtime確認済のみ
次:=提案／実行許可ではない
commit:=実行済commitまたは推奨message／自動commit許可ではない
```

`変更:`は当該run開始時と終了時の状態が異なるrepo相対pathを全件記載。開始dirtyでも今回不変なら含めない。renameは旧新path、deleteは旧path。検査できない場合は推測で完全一覧と断定しない。

この報告を仕様書／引継書／roadmapへ拡張しない。MarkSlot等の外部取込との実機互換性は、受領側で別途確認が必要。
