# KDSL Base Dev Prompt Template v2.0-kanji-canonical

```text
KDSL_PROMPT:
format: KDSL
profile: dev-prompt
mode: min
safety: normal

局面:
目的:
成功条件:
根拠:
正本:
権限:
承認境界:
対象:
非対象:
作業:
試験:
検証:
停止条件:
報告:
```

基本:

```text
漢字圧縮>要件保持>明示scope完走>必要最小限安全
共有材判可→AI丸投禁止
U観測>AI推測
1機能=1Phase
内部Slice完了→停止理由禁止
```

安全:

```text
明示criticalのみ保護
U未指定gate追加禁止
安全理由scope／Phase／architecture拡張禁止
追加hardening混入禁止
```

報告:

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
