def register_ok(x):
    return """
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Doğrulama</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background-color: #ffffff;
      margin: 0;
      padding: 0;
    }
    .email-container {
      width: 100%;
      background-color: #f9f9f9;
      padding: 30px 0;
    }
    .email-content {
      background-color: #ffffff;
      padding: 40px;
      border-radius: 8px;
      width: 100%;
      max-width: 600px;
      margin: 0 auto;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    }
    .email-header {
      text-align: center;
      margin-bottom: 20px;
    }
    .email-header i {
      font-size: 60px;
      color: #4CAF50;
    }
    .email-title {
      font-size: 28px;
      font-weight: 600;
      color: #333;
      margin-top: 10px;
    }
    .email-body {
      text-align: center;
      font-size: 18px;
      color: #333;
      line-height: 1.6;
    }
    .cta-button {
      display: inline-block;
      background-color: #007bff;
      color: #ffffff;
      padding: 15px 30px;
      text-decoration: none;
      border-radius: 5px;
      font-size: 18px;
      margin-top: 30px;
    }
    .footer {
      text-align: center;
      font-size: 14px;
      color: #999;
      margin-top: 30px;
    }
  </style>
</head>
<body>

  <div class="email-container">
    <div class="email-content">
      <div class="email-header">
        <i class="fas fa-check-circle"></i>
        <div class="email-title">DevHub.tr</div>
      </div>

      <div class="email-body">
        <h2 class="font-bold text-2xl text-gray-800">Hesabınız Başarıyla Doğrulandı!</h2>
        <p class="text-lg text-gray-700 mt-4">Hesabınız başarıyla doğrulandı! Artık platformda güvenle işlem yapabilirsiniz.</p>
        <a href="https://devhub.tr/auth" class="cta-button mt-6">Hesabınıza Giriş Yapın</a>
      </div>

      <div class="footer">
        <p class="text-sm text-gray-500 mt-6">Bu e-posta, platformumuza kaydolduğunuz için gönderilmiştir.</p>
        <p class="text-sm text-gray-500 mt-2">Bizimle iletişime geçmek için lütfen <a href="mailto:destek@devhub.tr" class="text-blue-600">destek@devhub.tr</a> adresine e-posta gönderin.</p>
      </div>
    </div>
  </div>

</body>
</html>
"""
def verify_email(link):
    return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Email Doğrulama</title>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Poppins', sans-serif;
      background-color: #f3f4f6;
      margin: 0;
      padding: 0;
    }}
    .email-container {{
      background-color: #ffffff;
      padding: 40px;
      border-radius: 8px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      max-width: 600px;
      margin: 0 auto;
    }}
    .email-header {{
      text-align: center;
      margin-bottom: 20px;
    }}
    .email-header h1 {{
      font-size: 24px;
      color: #333;
      margin-bottom: 10px;
    }}
    .email-body {{
      text-align: center;
      font-size: 16px;
      color: #333;
      line-height: 1.5;
    }}
    .cta-button {{
  display: inline-block;
  background-color: #007bff;
  color: #ffffff;  /* Buton yazısını beyaz yap */
  padding: 15px 30px;
  text-decoration: none;
  border-radius: 5px;
  font-size: 18px;
  margin-top: 30px;
  transition: background-color 0.3s ease;
}}

.cta-button:hover {{
  background-color: #0056b3;
}}

    .footer {{
      text-align: center;
      font-size: 14px;
      color: #777;
      margin-top: 20px;
    }}
  </style>
</head>
<body>

  <div class="email-container">
    <!-- Header -->
    <div class="email-header">
      <h1>Hesabınızı Doğrulamak İçin Tıklayın</h1>
    </div>

    <!-- Body -->
    <div class="email-body">
      <p>Merhaba,</p>
      <p>Hesabınızın güvenliğini sağlamak için e-posta adresinizi doğrulamanız gerekmektedir.</p>
      <p>Hesabınızı doğrulamak için aşağıdaki butona tıklayın:</p>
      <a href="https://test.devhub.tr/verify_mail_q/{link}" class="cta-button">E-posta Doğrulama Linki</a>
    </div>

    <!-- Footer -->
    <div class="footer">
      <p>Bu e-posta, platformumuza kaydolduğunuz için gönderilmiştir.</p>
      <p>Bizimle iletişime geçmek için <a href="mailto:destek@devhub.tr" class="text-blue-500">destek@devhub.tr</a> adresine e-posta gönderebilirsiniz.</p>
    </div>
  </div>

</body>
</html>
"""
def code_2fa(code):
  return f"""
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>2FA Doğrulama Kodu</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        .header {{
            text-align: center;
            background-color: #4CAF50;
            color: #ffffff;
            padding: 20px;
            border-radius: 8px 8px 0 0;
        }}
        .content {{
            padding: 20px;
            text-align: left;
        }}
        .content h2 {{
            color: #333333;
        }}
        .code {{
            background-color: #f4f4f9;
            border: 1px solid #ddd;
            padding: 15px;
            font-size: 20px;
            font-weight: bold;
            color: #333333;
            text-align: center;
            margin-top: 20px;
            border-radius: 4px;
        }}
        .footer {{
            margin-top: 20px;
            font-size: 14px;
            color: #888888;
            text-align: center;
        }}
        a {{
            color: #4CAF50;
            text-decoration: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>2 adımlı doğrulama etkin</h1>
        </div>
        <div class="content">
            <h2>Merhaba ,</h2>
            <p>Hesabınıza giriş yapabilmek için 2 faktörlü doğrulama (2FA) kodunuzu girmeniz gerekmektedir.</p>
            <p>Aşağıdaki doğrulama kodunu kullanarak işleminizi tamamlayabilirsiniz:</p>
            <div class="code">
                {code}
            </div>
            <p>Bu kod sadece 10 dakika boyunca geçerli olacaktır.</p>
            <p>Doğrulama kodu girildikten sonra hesabınıza erişim sağlanacaktır.</p>
        </div>
        <div class="footer">
            <p>Bu işlemi siz yapmadıysanız, lütfen <a href="mailto:destek@devhub.tr">bize bildirin</a>.</p>
            <p>Teşekkürler,<br> DevHub.tr Ekibi</p>
        </div>
    </div>
</body>
</html>
"""