# PsersonalCertificateAuthority
１分間のみ有効なワンタイムパスワードの認証システム  
  
GCPのCloud Functions用に作成した。  
Cloud FunctionsではGETとPOSTを両方有効にてして、パラメータの受け取りをしていたので、  
GETをコードを明示的に除去するように修正した。
