import win32com.client

class Email:

    def update_status(self, order_obj):
        mail_subject = 'Your order has been ' + order_obj.status.lower()

        recipient_name = order_obj.customer.first_name + ' ' + order_obj.customer.last_name
        ordered_items = [str(key['item']) + ' * ' + str(key['quantity']) for key in order_obj.product.ordered_items]
        ordered_items = '\n'.join(ordered_items)

        mail_body = 'Dear {},\n\n'\
                    'Your order of:\n'\
                    '   {}\n\n'\
                    'Is now {}'.format(recipient_name, ordered_items, order_obj.status)

        outlook = win32com.client.Dispatch("Outlook.Application")
        outlook_msg = outlook.CreateItem(0)
        outlook_msg.To = order_obj.customer.email

        outlook_msg.Subject = mail_subject
        outlook_msg.Body = mail_body
        try:
            outlook_msg.Display()
        except:
            print("Error occured trying to open outlook email - this could be because you have alerts open")
