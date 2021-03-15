import win32com.client


def update_status(order_instance, products_and_quantities):
    mail_subject = 'Your order has been ' + order_instance.status.lower()
    recipient_name = order_instance.customer.first_name + ' ' + order_instance.customer.last_name
    ordered_items = ["  " + str(key) + ' * ' + str(product_and_quantities[key])
                         for key in product_and_quantities]
    ordered_items = '\n'.join(ordered_items)
    date = order_instance.dispatched_date if order_instance.status == 'Dispatched' else order_instance.completed_date
    mail_body = 'Dear {},\n\n'\
                'Your order of:\n'\
                '{}\n\n'\
                'Was {} on: {}'.format(recipient_name, ordered_items, order_instance.status, date)

    outlook = win32com.client.Dispatch("Outlook.Application")
    outlook_msg = outlook.CreateItem(0)
    outlook_msg.To = order_instance.customer.email

    outlook_msg.Subject = mail_subject
    outlook_msg.Body = mail_body
    try:
        outlook_msg.Display()
    except:
        print("Error occured trying to open outlook email - this could be because you have alerts open")
