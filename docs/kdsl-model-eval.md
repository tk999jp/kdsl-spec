# KDSL 実モデル比較 — 小規模の実験手順

この追加ツールは既存の8例から、条件・承認・実機状態の4系統20問を作り、同一のモデル・同一質問で自然文／`min`／`dense`を比較する。

- quick: 各系統から正例／負例を1つずつ選択、8問×3モード＝24回。
- full: 20問×3モード＝60回。`--repeats 3`なら180回。
- 回答は「はい」「いいえ」の二値。正答率・未回答・同一問での劣化件数・APIのinput token実測を集計。
- テストコードのfixtureは**実モデルではない**。fixtureでの全問正解を実モデルの成績として報告しない。
- 今回の質問は引用promptの意味判断のみ。元promptの開発作業や削除操作を実行しない。

```bash
# 1. 実行なしで比較入力を作成（正解は入力JSONLに含めない）
python tools/validator/kdsl_model_eval.py prepare --out /tmp/kdsl_requests.jsonl

# 2. 実モデル呼出し。OPENAI_API_KEYを環境変数に設定した場合のみ可能
# API利用料金が発生。model名は実際に利用可能なモデルを指定すること
python tools/validator/kdsl_model_eval.py run --model YOUR_MODEL --out /tmp/kdsl_responses.jsonl

# 3. 採点
python tools/validator/kdsl_model_eval.py score --responses /tmp/kdsl_responses.jsonl \
  --out /tmp/kdsl_score.json

# 全問: prepare/run/score のすべてに --full を付ける
# 3回反復: prepare/run/score のすべてに --repeats 3 を付ける

# 4. 評価器そのものの回帰テスト（API不要）
python -m unittest discover -s tools/validator -p 'test_*.py' -v
```

**境界・注意:** OpenAI Responses APIの`POST /v1/responses`を使用。任意の外部モデルに未接続のため、実モデルの結果はまだない。モデル側の未完了・予期しない回答は正答にしない。JSONLに欠落・異モデル混入・重複・プロンプトのハッシュ不一致があれば、完全な比較成績は出さない。APIのtoken使用量が報告されなければtokenは未計測。比較対象は4例の二値解釈能力に限定され、コード改修品質、全8例の意味同等性、実機検証を証明しない。
