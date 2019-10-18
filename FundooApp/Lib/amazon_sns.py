import boto3

client = boto3.client('sns')
class notification():
    arn=""
    def create_topic(self,name,display_name,email_addr):
        print(name,"sns name")
        print(display_name,"sns display name")
        response = client.create_topic(
            Name=name,
            Attributes={
                'DisplayName': display_name
            }
        )
        print("before response")
        arn=response['TopicArn']
        print(arn)
        print("after publish")
        print("emaildasfdsgf",email_addr)
        print("cli",response)
        self.subscribe(email_addr,arn)


    def subscribe(self,email_addr,arn):
        print("inside our email",print)
        response = client.subscribe(
        TopicArn=str(arn),
        Protocol='email',
        Endpoint=str(email_addr),


        ReturnSubscriptionArn=True | False
    )
        print("new response", response)











        # token=str(response['SubscriptionArn'])
        # datasplit =token.split(':')
    #     print("daaatsplit",datasplit[6])
    #
    #     self.confirm_subscription(arn,datasplit[6])
    #
    #
    # def confirm_subscription(self,arn,token):
    #     response = client.confirm_subscription(
    #         TopicArn=str(arn),
    #         Token=str(token),
    #         # AuthenticateOnUnsubscribe='string'
    #     )



    def publish(self,message):
        response = client.publish(
            TopicArn=self.arn,
            Message=message,
            Subject='reminder from  Fundoo Notes',
            MessageStructure='string',
            MessageAttributes={
                'string': {
                    'DataType': 'string',
                    'StringValue': 'string',
                    'BinaryValue': b'bytes'
                }
            }
        )
