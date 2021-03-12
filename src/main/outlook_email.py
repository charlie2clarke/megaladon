import win32com.client


def update_status(order_obj):
    mail_subject = 'Your order has been ' + order_obj.status.lower()

    recipient_name = order_obj.customer.first_name + ' ' + order_obj.customer.last_name
    ordered_items = ['      ' + str(key['item']) + ' * ' + str(key['quantity']) for key in order_obj.product.ordered_items]
    ordered_items = '\n'.join(ordered_items)
    date = order_obj.dispatched_date if order_obj.status == 'Dispatched' else order_obj.completed_date

    mail_body = 'Dear {},\n\n'\
                'Your order of:\n'\
                '{}\n\n'\
                'Was {} on: {}'.format(recipient_name, ordered_items, order_obj.status, date)

    outlook = win32com.client.Dispatch("Outlook.Application")
    outlook_msg = outlook.CreateItem(0)
    outlook_msg.To = order_obj.customer.email

    outlook_msg.Subject = mail_subject
    outlook_msg.Body = mail_body
    try:
        outlook_msg.Display()
    except:
        print("Error occured trying to open outlook email - this could be because you have alerts open")
