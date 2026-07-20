from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Variant:
    header: str
    body: str


@dataclass(frozen=True)
class Concept:
    name: str
    natural: tuple[str, ...]
    min: tuple[str, ...]
    dense: tuple[str, ...]


SAMPLES = [
    {
        "id": "dev",
        "category": "AI coding",
        "natural": """あなたはMidFDの実装を担当するAI coding toolです。Browser一覧の表示単位でBytesを選択した場合に、KBへ丸めた値ではなくファイルの実際のバイト数を表示するよう修正してください。既存のKB表示とMB表示の計算方法、表示形式、単位切替動作は変更しないでください。まず現在の実装と関連テストを調べて原因を限定し、必要なproduction codeと関連テストだけを編集してください。対象テストを実行し、影響が及ぶ場合だけ必要な全体回帰も実行してください。build、test、lintの成功を実機確認済みとは扱わないでください。今回の作業ではstage、commit、pushを行わないでください。最終報告では、開始時からdirtyだっただけで今回内容が変化していないファイルを混入せず、今回Runで実際に変更したファイルを完全なリポジトリ相対パスで全件列挙してください。主要ファイルだけに省略しないでください。""",
        "min": Variant(
            "KDSL_PROMPT:\nformat: KDSL\nprofile: dev-prompt\nmode: min\nsafety: normal",
            """局面: MidFD Bytes表示補正
目的: Browser一覧でBytes選択時→実byte数表示
成功条件: Bytes=非丸めbyte／既存KB・MB計算・形式・切替維持
対象: 表示経路／関連test
作業: 現実装・test確認→原因限定→必要code・test編集→対象test→影響時のみ必要回帰
検証: build／test／lint pass != 実機確認
権限: 読取／編集／試験=可、stage／commit／push=禁止
報告: R1／変更=RunChanged完全repo相対path全件
禁止: 開始時dirty不変file混入／主要file省略""",
        ),
        "dense": Variant(
            "KDSL_PROMPT:\nformat:KDSL\nprofile:dev-prompt\nmode:dense\nsafety:normal",
            "局面:MidFD Bytes補正;目的:Bytes選択→実byte;成功:Bytes=非丸めbyte/KB・MB計算・形式・切替維持;対象:表示経路/関連test;作業:現実装・test確認→原因限定→必要code・test編集→対象test→影響時のみ回帰;検証:build/test/lint!=実機;権限:読取/編集/試験=可,stage/commit/push=禁止;報告:R1,変更=RunChanged完全repo相対path全件;禁止:開始dirty不変混入/主要file省略",
        ),
        "concepts": (
            Concept("Bytes実値", ("実際のバイト数",), ("実byte数",), ("実byte",)),
            Concept("KB・MB維持", ("KB表示", "MB表示"), ("KB・MB",), ("KB・MB",)),
            Concept("実機分離", ("実機確認済みとは扱わない",), ("!= 実機確認",), ("!=実機",)),
            Concept("commit禁止", ("commit", "行わない"), ("commit", "禁止"), ("commit", "禁止")),
            Concept("push禁止", ("push", "行わない"), ("push", "禁止"), ("push", "禁止")),
            Concept("dirty不変除外", ("dirty", "変化していない", "混入せず"), ("dirty不変file混入",), ("dirty不変混入",)),
            Concept("完全path", ("完全なリポジトリ相対パス", "全件"), ("完全repo相対path全件",), ("完全repo相対path全件",)),
        ),
    },
    {
        "id": "blog",
        "category": "業務／blog meta",
        "natural": """あなたは技術系ブログの編集者兼SEO担当者です。入力された記事本文だけを根拠に、ブログ公開時に使用するメタ情報を日本語で作成してください。出力する項目は、120字以内の要約、主要テーマ5件と各テーマの短い説明、SEOタイトル案5件、120字以内のメタディスクリプション、タグ5件から8件です。記事本文に書かれていない製品仕様、数値、企業関係、評価、将来予測などを追加しないでください。断定できない内容は断定せず、不明であることが記事上重要な場合だけ簡潔に示してください。誇張表現、煽り表現、クリックを誘うためだけの強い表現は避けてください。技術初心者にも意味が伝わる語彙を使い、各項目は短く実用的にしてください。思考過程や分析過程は出力せず、指定された項目以外の前置きや補足も付けないでください。""",
        "min": Variant(
            "format: KDSL\nprofile: compact-prompt\nmode: min\nsafety: normal",
            """目的: 技術blog本文→公開meta生成
材料: article_textのみ
出力: 要約120字以内／主要題5＋短説／SEO title案5／description120字以内／tag5-8
規則: 日本語／初心者可読／短実用
禁止: 入力外仕様・数値・関係・評価・予測追加／不明断定／誇張・煽り／思考過程／指定外前置・補足
不明: 記事上重要時のみ簡潔表示""",
        ),
        "dense": Variant(
            "format:KDSL;profile:compact-prompt;mode:dense;safety:normal",
            "目的:技術blog本文→公開meta;材料:article_text限定;出力:要約≤120字/主要題5+短説/SEO title5/description≤120字/tag5-8;規則:日本語/初心者可読/短実用;禁止:入力外仕様・数値・関係・評価・予測追加/不明断定/誇張・煽り/思考過程/指定外文;不明:重要時のみ簡潔表示",
        ),
        "concepts": (
            Concept("本文限定", ("記事本文だけ",), ("article_textのみ",), ("article_text限定",)),
            Concept("要約120字", ("120字以内の要約",), ("要約120字以内",), ("要約≤120字",)),
            Concept("主要題5", ("主要テーマ5件",), ("主要題5",), ("主要題5",)),
            Concept("tag5-8", ("タグ5件から8件",), ("tag5-8",), ("tag5-8",)),
            Concept("入力外禁止", ("追加しない",), ("入力外", "追加"), ("入力外", "追加")),
            Concept("誇張煽り禁止", ("誇張表現", "煽り表現", "避け"), ("誇張・煽り", "禁止"), ("誇張・煽り", "禁止")),
            Concept("思考非出力", ("思考過程", "出力せず"), ("思考過程", "禁止"), ("思考過程", "禁止")),
        ),
    },
    {
        "id": "creative",
        "category": "創作seed",
        "natural": """あなたはHIMADES系シナリオのためのシード抽出・再設計アシスタントです。ユーザーが入力した一行アイデア、ランダムテーマ、短い物語の種、既存作品のあらすじ、ニュース的な題材、技術・社会・心理・SFの概念から、HIMADES形式のシナリオ作成に適したシードを再構成してください。この段階では完成シナリオ、本文、会話台本、ショート動画用の完成稿を書かないでください。入力から、日常を崩す異常設定、人物を動かす感情の核、作中で観測できる事実、元の状態へ戻れなくなる不可逆の変化、物語の最後に残る状態を抽出してください。入力に書かれていない設定を確定事実として追加せず、推測や再設計案は推測または提案であることを明示してください。各項目は短く具体的にし、互いに同じ内容を言い換えて重複させないでください。最後に、抽出したシードをどの方向へシナリオ化できるか、互いに異なる方向性を3案だけ示してください。""",
        "min": Variant(
            "format: KDSL\nprofile: compact-prompt\nmode: min\nsafety: normal",
            """役割: HIMADES seed抽出・再設計
入力: 一行案／random題／物語種／既存作粗筋／news題／技術・社会・心理・SF概念
目的: 入力→HIMADES用seed
非出力: 完成scenario／本文／会話台本／short完成稿
抽出: 異常設定／感情核／観測事実／不可逆変化／終残状態
規則: 入力外設定を確定事実化禁止／推測・再設計案=明示／短具体／重複禁止
出力: 抽出5項／異方向scenario化3案""",
        ),
        "dense": Variant(
            "format:KDSL;profile:compact-prompt;mode:dense;safety:normal",
            "役割:HIMADES seed抽出・再設計;入力:一行案/random題/物語種/既存粗筋/news題/技術・社会・心理・SF概念;目的:入力→HIMADES seed;非出力:完成scenario/本文/会話台本/short完成稿;抽出:異常設定/感情核/観測事実/不可逆変化/終残状態;規則:入力外設定の事実化禁止/推測・再設計案明示/短具体/重複禁止;出力:5項+異方向scenario化3案",
        ),
        "concepts": (
            Concept("HIMADES seed", ("HIMADES", "シード"), ("HIMADES", "seed"), ("HIMADES", "seed")),
            Concept("完成稿非出力", ("完成シナリオ", "書かない"), ("完成scenario", "非出力"), ("完成scenario", "非出力")),
            Concept("抽出5項", ("異常設定", "感情の核", "観測できる事実", "不可逆の変化", "最後に残る状態"), ("異常設定", "感情核", "観測事実", "不可逆変化", "終残状態"), ("異常設定", "感情核", "観測事実", "不可逆変化", "終残状態")),
            Concept("入力外事実禁止", ("確定事実として追加せず",), ("確定事実化禁止",), ("事実化禁止",)),
            Concept("推測明示", ("推測", "明示"), ("推測", "明示"), ("推測", "明示")),
            Concept("重複禁止", ("重複させない",), ("重複禁止",), ("重複禁止",)),
            Concept("方向3案", ("方向性を3案",), ("scenario化3案",), ("scenario化3案",)),
        ),
    },
]


def compact_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def contains_all(text: str, markers: tuple[str, ...]) -> bool:
    return all(marker in text for marker in markers)


def reduction(base: int, value: int) -> float:
    return round((1 - value / base) * 100, 1)


def main() -> int:
    errors: list[str] = []
    total_natural = 0
    totals = {"min_body": 0, "min_total": 0, "dense_body": 0, "dense_total": 0}
    print("sample\tcategory\tnatural\tmin_body\tmin_total\tdense_body\tdense_total")
    for sample in SAMPLES:
        natural = sample["natural"]
        min_v: Variant = sample["min"]
        dense_v: Variant = sample["dense"]
        n = compact_length(natural)
        mb = compact_length(min_v.body)
        mt = compact_length(min_v.header + "\n" + min_v.body)
        db = compact_length(dense_v.body)
        dt = compact_length(dense_v.header + "\n" + dense_v.body)
        total_natural += n
        totals["min_body"] += mb
        totals["min_total"] += mt
        totals["dense_body"] += db
        totals["dense_total"] += dt
        if mb >= n:
            errors.append(f"{sample['id']}:min本文非圧縮")
        if db >= n:
            errors.append(f"{sample['id']}:dense本文非圧縮")
        if reduction(n, mt) < 15:
            errors.append(f"{sample['id']}:min投入全体削減15%未満")
        if reduction(n, dt) < 15:
            errors.append(f"{sample['id']}:dense投入全体削減15%未満")
        for concept in sample["concepts"]:
            for label, text, markers in (
                ("natural", natural, concept.natural),
                ("min", min_v.body, concept.min),
                ("dense", dense_v.body, concept.dense),
            ):
                if not contains_all(text, markers):
                    errors.append(f"{sample['id']}:{label}:概念欠落:{concept.name}")
        print(f"{sample['id']}\t{sample['category']}\t{n}\t{mb}\t{mt}\t{db}\t{dt}")

    print(
        "TOTAL"
        f"\tnatural={total_natural}"
        f"\tmin_body={totals['min_body']}({reduction(total_natural, totals['min_body'])}%)"
        f"\tmin_total={totals['min_total']}({reduction(total_natural, totals['min_total'])}%)"
        f"\tdense_body={totals['dense_body']}({reduction(total_natural, totals['dense_body'])}%)"
        f"\tdense_total={totals['dense_total']}({reduction(total_natural, totals['dense_total'])}%)"
    )
    print("TOKEN model-dependent/not-measured")
    if errors:
        for error in errors:
            print("ERROR", error)
        return 1
    print("PASS samples=3 concepts=21 metric=non-whitespace-unicode-codepoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
