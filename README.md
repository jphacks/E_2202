![backend ci workflow](https://github.com/jphacks/E_2202/actions/workflows/python-code-check.yml/badge.svg) 
![frontend workflow](https://github.com/jphacks/E_2202/actions/workflows/heroku-dev-frontend.yml/badge.svg) 

# YouQuery (Error × tech)
[!['YouQueryデモ動画'](https://user-images.githubusercontent.com/33239413/201500067-67884b89-7c86-4cba-8080-24b4a56e15e2.png)](https://youtu.be/YaftNA4aTt8)

## 製品概要
### 背景(製品開発のきっかけ、課題等）
プログラミングを始めたての頃は、エラー文が出ると「**どこの部分を読んで検索をすればいいのか分からない！**」という経験をしたと思います。
エラーがいつまでも解決できない経験をすると、**プログラミングに対して苦手意識**を持ってしまい、**初学者のモチベーションの低下**につながります。
その課題に対して、長いエラー文の中から解決につながる単語を提案したり、実際のエラー文から重要な単語をハイライト表示したりすることで、**初学者のエラー解決**をサポートします。

### 製品説明（具体的な製品の説明）
エラー文をYouQueryに貼ることで、言語や環境に合わせてエラー文を解析し、より良い検索ができるようなエラー文を提案いたします。また、実際のエラー文で重要な箇所を強調表示する機能があり、これにより初学者は「解決するための手かがりの探し方」を学ぶことができます。

### 特長
* Googleで検索するための検索クエリを自動で出力してくれます。
* ユーザーが貼ったエラー文の中から重要な箇所をハイライト表示することができます。

### 解決出来ること
* 長いエラー文の中から重要な情報だけを抜き出し検索することができます。
* エラー文の中で重要な情報だけをハイライトすることができ、どの部分のエラーを読めばいいのかを知ることができます。

### 今後の展望
* より多くの言語のエラー文にも対応していきます。
* エラー文や検索についての理解や様々な方からのフィードバックをいただき、解析や検索のクオリティの向上を目指す。

### 注力したこと（こだわり等）
* 発表日までにMVPを作成しデプロイしました。
* 言語によって解析方法を変えています。

## 開発技術

### 開発手法
- テスト駆動開発

### 活用した技術
- フロントエンド
  - TypeScript
  - Next.js
 
- バックエンド
  - Python
  - FastAPI
  - doctest
  - Pytest
  - mypy
  - Flake8
  - black
  
- インフラ
  - Heroku
  - GitHub Actions

### 独自技術
#### ハッカソンで開発した独自機能・技術
- エラー文を解析する機能
  - この機能では、**正規表現**にてエラー文の着目する箇所を抽出しました。
  - 競合する技術として、**BERTなどの大規模言語モデル**を用いて文の重要箇所を抽出する方法がありました。
  - ただ、Pythonのエラー文解析にはオーバースペックであるという点と、1週間という開発期間の中でMVPを作成することを目標とした点で、
  正規表現で抽出する方法が適していると考えました。
  - 今後は複数のプログラミング言語やライブラリに対応できるように、機械学習を用いて機能のアップデートを続けていきたいです。


