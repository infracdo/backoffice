import mandrill

class MandrillInterface:

    def set_api_key(self, api_key, from_name, from_email):
        self.api_key = api_key
        self.from_name = from_name
        self.from_email = from_email
        self.mandrill_client = mandrill.Mandrill(self.api_key)

    def send_mail(self,to_email,subject,message,attachments=[],images=[],schedule=''):

        message = {
            'from_email': "no-reply@thousandminds.com",
            'from_name': "Zeep Team",
            'to': [{
                'email': to_email,
                'type': 'to'
            }],
            'subject': subject,
            'text': message
        }

        if self.from_name: message['from_name'] = self.from_name
        if self.from_email: message['from_email'] = self.from_email
        if attachments: message['attachments'] = attachments
        if images: message['images'] = images
        if schedule: message['send_at'] = schedule

        result = self.mandrill_client.messages.send(message = message)
        return result
    
    def email_verification(self, args):
        message = {
            'from_email': "no-reply@thousandminds.com",
            'from_name': "Zeep Team",
            'to': [{
                'email': args['email'],
                'type': 'to'
            }],
            'subject': "Email Verification",
            'html': self.get_verification_content(args)
        }

        if self.from_name: message['from_name'] = self.from_name
        if self.from_email: message['from_email'] = self.from_email
        result = self.mandrill_client.messages.send(message = message)
        return result     

    def get_verification_content(self, args):
        verify_url = f"{self.verification_url}/{args['otp_id']}/{args['otp']}"
        content = """
            <!DOCTYPE html> 
            <html> 
                <head>
                    <link rel="stylesheet" type="text/css">
                    <style>
                        .btn-primary {
                            color: #fff;
                            background-color: #337ab7;
                            border-color: #2e6da4;

                        }
                        .btn {
                            display: inline-block;
                            width: 80px;
                            margin-bottom: 0;
                            font-weight: 400;
                            text-align: center;
                            white-space: nowrap;
                            vertical-align: middle;
                            -ms-touch-action: manipulation;
                            touch-action: manipulation;
                            cursor: pointer;
                            background-image: none;
                            border: 1px solid transparent;
                            padding: 6px 12px;
                            font-size: 14px;
                            line-height: 1.42857143;
                            border-radius: 4px;
                            -webkit-user-select: none;
                            -moz-user-select: none;
                            -ms-user-select: none;
                            user-select: none;
                        }
                        .main {
                            flex-direction: column;
                        }
                    </style>
                </head>
            """

        content += f"""
                <body>
                    <div class="main" style="flex-direction: column;">
                        <p> Hi {args.get('fullname')}, </p>
                        
                        <p> Please verify your email address by clicking verify. </p>
                        
                        <button class="btn btn-primary">
                            <a href={verify_url} style="color:#fff; text-decoration: none;">
                            Verify
                            </a>
                        </button>
                        
                        <p style="margin-bottom: 0;">
                            Note: The link is only active for 24 hours. If you are unable to use the verify button, click the link below or copy and paste it into the address bar of your web browser.
                        </p>
                        <a href={verify_url}>{verify_url} </a>

                        <p>If you didn't sign-up with this address, you can ignore this email.</p>

                        <p style="margin-bottom: 0;">Thanks!</p>
                        <p style="margin-top: 0;">Packworks Inventory Financing Team</p>
                    </div>
                </body>
            </html>
        """
        return content

mailer = MandrillInterface()
